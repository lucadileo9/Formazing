"""
🎯 Training Service - Orchestratore per operazioni formazioni

Centralizza tutta la logica business per:
- Preview messaggi
- Invio comunicazioni  
- Gestione feedback
- Generazione codici
- Aggiornamenti stati

Separazione netta tra controllo HTTP (routes) e business logic (questo service).
"""

import logging
from typing import Dict, List, Optional
from app.services.notion import NotionService, NotionServiceError
from app.services.telegram_service import TelegramService
from config import Config

logger = logging.getLogger(__name__)


class TrainingServiceError(Exception):
    """Eccezione specifica per errori TrainingService."""
    pass


class TrainingService:
    """
    Orchestratore principale per operazioni su formazioni.
    
    Separa la logica business dai route Flask per:
    - Maggiore testabilità
    - Riutilizzo del codice
    - Separazione responsabilità
    - Error handling centralizzato
    """
    
    def __init__(self):
        """Inizializza servizi dipendenti."""
        self.notion_service = NotionService()
        self.telegram_service = TelegramService(
            token=Config.TELEGRAM_BOT_TOKEN,
            groups_config_path=Config.TELEGRAM_GROUPS_CONFIG,
            templates_config_path=Config.TELEGRAM_TEMPLATES_CONFIG
        )
        logger.info("TrainingService inizializzato con NotionService e TelegramService")
    
    async def generate_preview(self, training_id: str) -> Dict:
        """
        Genera anteprima completa per una formazione.
        
        Validazioni:
        - Formazione deve esistere
        - Stato deve essere "Programmata"
        
        Args:
            training_id: ID della formazione da Notion
            
        Returns:
            Dict con preview data: {
                'training': dict formazione,
                'messages': [{'area': 'IT', 'chat_id': -123, 'message': '...'}, ...],
                'codice_generato': str codice generato,
                'email': dict (opzionale)
            }
            
        Raises:
            TrainingServiceError: Se formazione non valida per preview
        """
        try:
            logger.info(f"Generazione preview per formazione {training_id}")
            
            # Recupera e valida formazione
            training = await self.notion_service.get_formazione_by_id(training_id)
            if not training:
                raise TrainingServiceError(f"Formazione {training_id} non trovata")
                
            if training.get('Stato') != 'Programmata':
                raise TrainingServiceError(
                    f"Solo formazioni 'Programmata' possono essere processate (stato attuale: {training.get('Stato')})"
                )
            
            # Genera codice
            generated_code = self._generate_training_code(training)
            
            # Genera messaggi preview per ogni area
            messages_preview = []
            for area in training.get('Area', []):
                # Verifica se l'area ha un gruppo configurato
                if area in self.telegram_service.groups:
                    chat_id = self.telegram_service.groups[area]
                    # Usa formatters per generare messaggio
                    message = self.telegram_service.formatter.format_training_message(training, group_key=area)
                    messages_preview.append({
                        'area': area,
                        'chat_id': chat_id,
                        'message': message
                    })
            
            # Aggiungi anche main_group se presente
            if 'main_group' in self.telegram_service.groups and training.get('Periodo') != 'OUT':
                main_chat_id = self.telegram_service.groups['main_group']
                main_message = self.telegram_service.formatter.format_training_message(training, group_key='main_group')
                messages_preview.append({
                    'area': 'Main Group',
                    'chat_id': main_chat_id,
                    'message': main_message
                })
            
            preview_data = {
                'training': training,
                'messages': messages_preview,
                'codice_generato': generated_code,
                # TODO: Aggiungere preview email quando integrazione Graph API sarà pronta
                'email': None
            }
            
            logger.info(f"Preview generata con successo per {training.get('Nome', 'N/A')} con {len(messages_preview)} messaggi")
            return preview_data
            
        except NotionServiceError as e:
            logger.error(f"Errore Notion in preview {training_id}: {e}")
            raise TrainingServiceError(f"Errore accesso dati: {e}")
        except Exception as e:
            logger.error(f"Errore imprevisto in preview {training_id}: {e}")
            raise TrainingServiceError(f"Errore interno: {e}")
    
    async def send_training_notification(self, training_id: str) -> Dict:
        """
        Workflow completo per invio comunicazione formazione.
        
        Steps atomici:
        1. Valida formazione (stato "Programmata")
        2. Genera codice univoco e Teams link
        3. Aggiorna stato Notion → "Calendarizzata"
        4. Invia messaggi Telegram ai gruppi target
        
        Args:
            training_id: ID della formazione da Notion
            
        Returns:
            Dict con risultati operazione: {
                'codice_generato': str,
                'teams_link': str,
                'telegram_results': dict,
                'nuovo_stato': str
            }
            
        Raises:
            TrainingServiceError: Se operazione fallisce
        """
        try:
            logger.info(f"Avvio invio comunicazione per formazione {training_id}")
            
            # Valida formazione
            training = await self.notion_service.get_formazione_by_id(training_id)
            if not training:
                raise TrainingServiceError(f"Formazione {training_id} non trovata")
                
            if training.get('Stato') != 'Programmata':
                raise TrainingServiceError("Formazione già processata o stato non valido")
            
            # Genera codice e Teams link
            generated_code = self._generate_training_code(training) 
            teams_link = await self._create_teams_meeting(training)
            
            # Aggiorna Notion PRIMA dell'invio (per consistenza) - USA METODO UNIFICATO
            await self.notion_service.update_formazione(training_id, {
                'Codice': generated_code,
                'Link Teams': teams_link,
                'Stato': 'Calendarizzata'
            })
            
            # Recupera formazione aggiornata per invio
            updated_training = await self.notion_service.get_formazione_by_id(training_id)
            
            # Invia messaggi Telegram
            send_results = await self.telegram_service.send_training_notification(updated_training)
            
            result = {
                'codice_generato': generated_code,
                'teams_link': teams_link,
                'telegram_results': send_results,
                'nuovo_stato': 'Calendarizzata'
            }
            
            logger.info(f"Comunicazione inviata con successo: {updated_training.get('Nome', 'N/A')} - Codice: {generated_code}")
            return result
            
        except NotionServiceError as e:
            logger.error(f"Errore Notion in send {training_id}: {e}")
            raise TrainingServiceError(f"Errore aggiornamento dati: {e}")
        except Exception as e:
            logger.error(f"Errore imprevisto in send {training_id}: {e}")
            raise TrainingServiceError(f"Errore invio: {e}")
    
    async def generate_feedback_preview(self, training_id: str) -> Dict:
        """
        Genera anteprima richiesta feedback senza inviare nulla.
        
        Validazioni:
        - Formazione deve esistere
        - Stato deve essere "Calendarizzata"
        - Deve avere un codice generato
        
        Args:
            training_id: ID della formazione da Notion
            
        Returns:
            Dict con struttura:
            {
                'training': {...},
                'messages': [{'area': 'IT', 'chat_id': -123, 'message': '...'}, ...]
            }
            
        Raises:
            TrainingServiceError: Se formazione non valida per feedback
        """
        try:
            logger.info(f"🔍 Generazione preview feedback per {training_id}")
            
            # 1️⃣ Recupera dati formazione
            training = await self.notion_service.get_formazione_by_id(training_id)
            if not training:
                raise TrainingServiceError(f"Formazione {training_id} non trovata")
            
            # ⚠️ Validazione: deve essere Calendarizzata
            if training.get('Stato') != 'Calendarizzata':
                raise TrainingServiceError(
                    f"La formazione deve essere 'Calendarizzata'. Stato attuale: {training.get('Stato')}"
                )
            
            # ⚠️ Validazione: deve avere codice
            if not training.get('Codice'):
                raise TrainingServiceError("La formazione non ha un codice generato")
            
            # 2️⃣ Genera messaggi preview (senza invio)
            messages_preview = []
            
            # Genera link feedback temporaneo per preview
            feedback_link = self._generate_feedback_link(training)
            
            # ⚠️ IMPORTANTE: Feedback va SOLO ai gruppi area (NO main_group)
            # Ottieni target groups e rimuovi main_group
            all_target_groups = self.telegram_service._get_target_groups(training)
            target_groups = [group for group in all_target_groups if group != 'main_group']
            
            for group_key in target_groups:
                if group_key in self.telegram_service.groups:
                    chat_id = self.telegram_service.groups[group_key]
                    # Usa formatter esistente per feedback (richiede feedback_link e group_key)
                    message = self.telegram_service.formatter.format_feedback_message(
                        training, 
                        feedback_link, 
                        group_key=group_key
                    )
                    messages_preview.append({
                        'area': group_key,
                        'chat_id': chat_id,
                        'message': message
                    })
            
            logger.info(f"✅ Preview feedback generata con {len(messages_preview)} messaggi (solo gruppi area)")
            
            return {
                'training': training,
                'messages': messages_preview
            }
            
        except TrainingServiceError:
            raise
        except Exception as e:
            logger.error(f"Errore in generate_feedback_preview: {e}")
            raise TrainingServiceError(f"Errore generazione preview feedback: {e}")
    
    async def send_feedback_request(self, training_id: str) -> Dict:
        """
        Invia richiesta feedback post-formazione.
        
        Steps:
        1. Valida formazione (stato "Calendarizzata")
        2. Genera link feedback personalizzato
        3. Invia via Telegram con template feedback
        4. Aggiorna stato → "Conclusa"
        
        Args:
            training_id: ID della formazione da Notion
            
        Returns:
            Dict con risultati operazione: {
                'feedback_link': str,
                'telegram_results': dict,
                'nuovo_stato': str
            }
            
        Raises:
            TrainingServiceError: Se operazione fallisce
        """
        try:
            logger.info(f"Avvio invio feedback per formazione {training_id}")
            
            # Valida formazione
            training = await self.notion_service.get_formazione_by_id(training_id)
            if not training:
                raise TrainingServiceError(f"Formazione {training_id} non trovata")
                
            if training.get('Stato') != 'Calendarizzata':
                raise TrainingServiceError("Formazione non ancora calendarizzata")
            
            # Genera link feedback
            feedback_link = self._generate_feedback_link(training) # TODO: TROVARE UN MODO PER PRENDERE IL LINK VERO
            
            # Invia feedback via Telegram
            send_results = await self.telegram_service.send_feedback_notification(training, feedback_link)
            
            # Aggiorna stato a Conclusa
            await self.notion_service.update_formazione(training_id, {
                'Stato': 'Conclusa'
            })
            
            result = {
                'feedback_link': feedback_link,
                'telegram_results': send_results,
                'nuovo_stato': 'Conclusa'
            }
            
            logger.info(f"Feedback inviato con successo: {training.get('Nome', 'N/A')}")
            return result
            
        except NotionServiceError as e:
            logger.error(f"Errore Notion in feedback {training_id}: {e}")
            raise TrainingServiceError(f"Errore aggiornamento dati: {e}")
        except Exception as e:
            logger.error(f"Errore imprevisto in feedback {training_id}: {e}")
            raise TrainingServiceError(f"Errore invio feedback: {e}")
    
    # === PRIVATE UTILITY METHODS ===
    
    def _generate_training_code(self, training: Dict) -> str:
        """
        Genera codice formazione univoco.
        
        Formato: {Area}-{Nome}-{Anno}-{Periodo}-{Sequenza}
        Esempio: IT-Security_Training-2024-SPRING-01
        """
        # Area può essere lista o stringa - gestisci entrambi i casi
        area_raw = training.get('Area', ['IT'])
        if isinstance(area_raw, list):
            area = area_raw[0] if area_raw else 'IT'
        else:
            area = area_raw
        
        nome = training.get('Nome', 'Formazione').replace(' ', '_').replace('-', '_')
        periodo = training.get('Periodo', 'ONCE')
        anno = '2024'  # TODO: datetime.now().year
        
        # TODO: Implementare sequenza intelligente basata su database
        sequenza = '01'
        
        code = f"{area}-{nome}-{anno}-{periodo}-{sequenza}"
        logger.debug(f"Codice generato: {code}")
        return code
    
    async def _create_teams_meeting(self, training: Dict) -> str:
        """
        Crea meeting Teams tramite Microsoft Graph API.
        
        TODO: Implementare integrazione reale con Microsoft Graph.
        Per ora ritorna placeholder URL.
        """
        # Placeholder - da sostituire con Microsoft Graph API
        nome_safe = training.get('Nome', 'formazione').replace(' ', '-').lower()
        teams_link = f"https://teams.microsoft.com/meeting-{nome_safe}"
        
        logger.debug(f"Teams link generato (placeholder): {teams_link}")
        return teams_link
    
    def _generate_feedback_link(self, training: Dict) -> str:
        """
        Genera link feedback personalizzato.
        
        TODO: Integrare con sistema reale di raccolta feedback.
        Utilizza il codice formazione per creare URL univoco.
        """
        codice = training.get('Codice', 'placeholder')
        feedback_link = f"https://forms.office.com/feedback-{codice}"
        
        logger.debug(f"Feedback link generato: {feedback_link}")
        return feedback_link