"""
🎯 Training Service - Orchestratore per operazioni formazioni

Centralizza tutta la logica business per:
- Preview messaggi
- Invio comunicazioni  
- Gestione feedback
- Generazione codici
- Aggiornamenti stati

Separazione netta tra controllo HTTP (routes) e business logic (questo service).

DESIGN PATTERN: Singleton
- Garantisce una sola istanza per tutta la vita dell'app
- Bot Telegram sempre online (no restart continui)
- Riutilizzo connessioni Notion/Microsoft/Telegram
"""

import logging
import os
import threading
import asyncio
from datetime import datetime
from typing import Dict, List, Optional
from app.services.notion import NotionService, NotionServiceError
from app.services.telegram_service import TelegramService
from app.services.microsoft import MicrosoftService, MicrosoftServiceError
from config import Config

logger = logging.getLogger(__name__)


class TrainingServiceError(Exception):
    """Eccezione specifica per errori TrainingService."""
    pass


class TrainingService:
    """
    Orchestratore principale per operazioni su formazioni.
    
    DESIGN PATTERN: Singleton
    - Una sola istanza per tutta la vita dell'applicazione
    - Bot Telegram sempre online senza restart
    - Thread-safe per ambienti multi-worker
    
    Separa la logica business dai route Flask per:
    - Maggiore testabilità
    - Riutilizzo del codice
    - Separazione responsabilità
    - Error handling centralizzato
    """
    
    # Singleton state
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """Garantisce una sola istanza (thread-safe)."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-checked locking
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Inizializza servizi dipendenti UNA SOLA VOLTA."""
        # Evita reinizializzazione se già fatto
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        
        logger.info("🎯 Inizializzazione TrainingService (Singleton)")
        
        # Inizializza servizi dipendenti
        self.notion_service = NotionService()
        self.telegram_service = TelegramService(
            token=Config.TELEGRAM_BOT_TOKEN,
            notion_service=self.notion_service,
            groups_config_path=Config.TELEGRAM_GROUPS_CONFIG,
            templates_config_path=Config.TELEGRAM_TEMPLATES_CONFIG
        )
        self.microsoft_service = MicrosoftService()
        
        logger.info("TrainingService inizializzato con NotionService, TelegramService e MicrosoftService")

    @classmethod
    def get_instance(cls):
        """
        Factory method per ottenere istanza singleton.
        
        Usage nelle routes:
            training_service = TrainingService.get_instance()
        """
        return cls()
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
                'email': {
                    'attendee_emails': ['it@jemore.it', ...],
                    'subject': 'Oggetto email',
                    'body_preview': 'Anteprima corpo email...'
                }
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
            generated_code = self._generate_training_code(training, write=False)
            
            # Aggiungi codice temporaneamente per preview
            training_preview = training.copy()
            training_preview['Codice'] = generated_code
            
            # Genera messaggi preview Telegram per ogni area
            messages_preview = []
            for area in training.get('Area', []):
                # Verifica se l'area ha un gruppo configurato
                if area in self.telegram_service.groups:
                    chat_id = self.telegram_service.groups[area]
                    # Usa formatters per generare messaggio
                    message = self.telegram_service.formatter.format_training_message(training_preview, group_key=area)
                    messages_preview.append({
                        'area': area,
                        'chat_id': chat_id,
                        'message': message
                    })
            
            # Aggiungi anche main_group se presente
            if 'main_group' in self.telegram_service.groups and training.get('Periodo') != 'OUT':
                main_chat_id = self.telegram_service.groups['main_group']
                main_message = self.telegram_service.formatter.format_training_message(training_preview, group_key='main_group')
                messages_preview.append({
                    'area': 'Main Group',
                    'chat_id': main_chat_id,
                    'message': main_message
                })
            
            # Genera preview email usando MicrosoftService
            email_preview = None
            try:
                # Ottieni destinatari email dalle aree
                attendee_emails = self.microsoft_service.calendar_operations._get_attendee_emails_for_areas(
                    training.get('Area', [])
                )
                
                # Genera subject e body preview
                subject = self.microsoft_service.email_formatter.format_subject(training_preview)
                body_preview = self.microsoft_service.email_formatter.format_calendar_body(training_preview)
                                
                email_preview = {
                    'attendee_emails': attendee_emails,
                    'subject': subject,
                    'body_preview': body_preview  
                }
                
                logger.debug(f"Email preview generata - Destinatari: {', '.join(attendee_emails)}")
                
            except Exception as e:
                logger.warning(f"Impossibile generare preview email: {e}")
                # Preview email opzionale - se fallisce, procedi comunque
                email_preview = {
                    'error': str(e),
                    'attendee_emails': [],
                    'subject': 'N/A',
                    'body_preview': 'Errore generazione preview'
                }
            
            preview_data = {
                'training': training,
                'messages': messages_preview,
                'codice_generato': generated_code,
                'email': email_preview
            }
            
            logger.info(
                f"Preview generata con successo per {training.get('Nome', 'N/A')} - "
                f"Telegram: {len(messages_preview)} messaggi - "
                f"Email: {len(email_preview.get('attendee_emails', []))} destinatari"
            )
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
        2. Genera codice univoco
        3. Crea evento Teams e invia email (Microsoft Graph API) - FAIL-FAST se fallisce
        4. Aggiorna stato Notion → "Calendarizzata" con codice e link Teams
        5. Invia messaggi Telegram ai gruppi target
        
        Args:
            training_id: ID della formazione da Notion
            
        Returns:
            Dict con risultati operazione: {
                'codice_generato': str,
                'teams_link': str,
                'attendee_emails': List[str],
                'telegram_results': dict,
                'nuovo_stato': str
            }
            
        Raises:
            TrainingServiceError: Se operazione fallisce
            MicrosoftServiceError: Se creazione evento Teams fallisce (fail-fast)
        """
        try:
            logger.info(f"Avvio invio comunicazione per formazione {training_id}")
            
            # 1. Valida formazione
            training = await self.notion_service.get_formazione_by_id(training_id)
            if not training:
                raise TrainingServiceError(f"Formazione {training_id} non trovata")
                
            if training.get('Stato') != 'Programmata':
                raise TrainingServiceError("Formazione già processata o stato non valido")
            
            # 2. Genera codice
            generated_code = self._generate_training_code(training)
            
            # Aggiungi codice alla formazione per passarlo a Microsoft
            training['Codice'] = generated_code
            
            # 3. Crea evento Teams + invia email (FAIL-FAST se fallisce)
            try:
                microsoft_result = await self._create_teams_meeting(training)
                teams_link = microsoft_result['teams_link']
                attendee_emails = microsoft_result['attendee_emails']
                logger.info(f"Microsoft integration completata - Email inviate a: {', '.join(attendee_emails)}")
            except MicrosoftServiceError as e:
                # FAIL-FAST: Se Microsoft fallisce, non proseguiamo
                logger.error(f"FAIL-FAST: Creazione evento Microsoft fallita per {training_id}: {e}")
                raise TrainingServiceError(f"Impossibile creare evento Teams: {e}")
            
            # 4. Aggiorna Notion con codice + link Teams + stato
            await self.notion_service.update_formazione(training_id, {
                'Codice': generated_code,
                'Link Teams': teams_link,
                'Stato': 'Calendarizzata'
            })
            
            # 5. Recupera formazione aggiornata per invio Telegram
            updated_training = await self.notion_service.get_formazione_by_id(training_id)
            
            # 6. Invia messaggi Telegram
            send_results = await self.telegram_service.send_training_notification(updated_training)
            
            result = {
                'codice_generato': generated_code,
                'teams_link': teams_link,
                'attendee_emails': attendee_emails,
                'telegram_results': send_results,
                'nuovo_stato': 'Calendarizzata'
            }
            
            logger.info(
                f"Comunicazione inviata con successo: {updated_training.get('Nome', 'N/A')} - "
                f"Codice: {generated_code} - Email: {len(attendee_emails)} - "
                f"Telegram: {len(send_results.get('sent', []))} messaggi"
            )
            return result
            
        except NotionServiceError as e:
            logger.error(f"Errore Notion in send {training_id}: {e}")
            raise TrainingServiceError(f"Errore aggiornamento dati: {e}")
        except MicrosoftServiceError:
            # Già loggato e wrappato sopra, propaga
            raise
        except TrainingServiceError:
            # Già loggato, propaga
            raise
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
            feedback_link = self._generate_feedback_link()
            
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
            
            logger.info(f"STEP 1: Recupero dati formazione da Notion per {training_id}")
            training = await self.notion_service.get_formazione_by_id(training_id)
            if not training:
                raise TrainingServiceError(f"Formazione {training_id} non trovata")
            logger.info(f"STEP 1 OK: Dati recuperati: {training.get('Nome')}")

            logger.info(f"STEP 2: Validazione stato formazione per {training_id}")
            if training.get('Stato') != 'Calendarizzata':
                raise TrainingServiceError(f"Formazione non ancora calendarizzata. Stato attuale: {training.get('Stato')}")
            logger.info("STEP 2 OK: Stato 'Calendarizzata' confermato.")

            logger.info(f"STEP 3: Generazione link feedback per {training_id}")
            feedback_link = self._generate_feedback_link()
            logger.info(f"STEP 3 OK: Link generato: {feedback_link}")

            logger.info(f"STEP 4: Invio notifica feedback via Telegram per {training_id}")
            send_results = await self.telegram_service.send_feedback_notification(training, feedback_link)
            logger.info(f"STEP 4 OK: Risultati invio Telegram: {send_results}")

            logger.info(f"STEP 5: Aggiornamento stato Notion a 'Conclusa' per {training_id}")
            await self.notion_service.update_formazione(training_id, {
                'Stato': 'Conclusa'
            })
            logger.info("STEP 5 OK: Stato aggiornato in Notion.")

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
            logger.error(f"Errore imprevisto in feedback {training_id}: {e}", exc_info=True)
            raise TrainingServiceError(f"Errore invio feedback: {e}")
    
    # === PRIVATE UTILITY METHODS ===
    
    def _generate_training_code(self, training: Dict, write: bool = True) -> str:
        """
        Genera codice formazione univoco.
        Il booleano 'write' indica se salvare il contatore (True per invio reale, False per preview).
        
        Formato: {Area}-{Nome}-{Anno}-{Periodo}-{Sequenza}
        Esempio: IT-Security_Training-2024-SPRING-01
        """
        # File per il contatore di sequenza
        counter_file = os.path.join(Config.BASE_DIR, 'sequence_counter.txt')

        # Leggi il contatore corrente, incrementalo e salvalo
        try:
            with open(counter_file, 'r') as f:
                current_sequence = int(f.read().strip())
        except FileNotFoundError:
            current_sequence = 0

        next_sequence = current_sequence + 1

        # Salva il contatore aggiornato solo se in modalità reale
        if write:
            with open(counter_file, 'w') as f:
                f.write(str(next_sequence))

        # Area può essere lista o stringa - gestisci entrambi i casi
        area_raw = training.get('Area', ['IT'])
        if isinstance(area_raw, list):
            area = area_raw[0] if area_raw else 'IT'
        else:
            area = area_raw
        
        nome = training.get('Nome', 'Formazione').replace(' ', '_').replace('-', '_')
        periodo = training.get('Periodo', 'ONCE')
        anno = str(datetime.now().year)
        sequenza = str(next_sequence).zfill(2)
        
        code = f"{area}-{nome}-{anno}-{periodo}-{sequenza}"
        logger.debug(f"Codice generato: {code}")
        return code
    
    async def _create_teams_meeting(self, training: Dict) -> Dict:
        """
        Crea meeting Teams tramite Microsoft Graph API.
        
        Integrazione reale con MicrosoftService per:
        - Creare evento calendario
        - Generare Teams meeting link
        - Inviare email a mailing list area
        
        Args:
            training: Dict con dati formazione (deve includere Nome, Data/Ora, Area, Codice)
            
        Returns:
            Dict con:
                - teams_link: str (URL meeting Teams)
                - event_id: str (ID evento calendario)
                - attendee_emails: List[str] (email destinatari)
                - calendar_link: str (link calendario Outlook)
                
        Raises:
            MicrosoftServiceError: Se creazione evento fallisce
        """
        try:
            logger.info(f"Creazione evento Teams per: {training.get('Nome', 'N/A')}")
            
            # Chiama MicrosoftService per creare evento completo
            result = await self.microsoft_service.create_training_event(training)
            
            logger.info(
                f"Evento Teams creato con successo - "
                f"Link: {result['teams_link'][:50]}... - "
                f"Email inviate a: {', '.join(result['attendee_emails'])}"
            )
            
            return result
            
        except MicrosoftServiceError as e:
            logger.error(f"Errore Microsoft Graph API: {e}")
            raise  # Propaga l'errore per fail-fast
        except Exception as e:
            logger.error(f"Errore imprevisto in creazione Teams meeting: {e}")
            raise MicrosoftServiceError(f"Errore creazione evento: {e}")
    
    def _generate_feedback_link(self) -> str:
        """
        Alla fine inviamo sempre lo stesso link di feedback.
        Sarà l'utente ad inserire il codice formazione nel form.

        Returns:
            str: Link di feedback
        """

        feedback_link = "https://forms.office.com/e/6dbjt4hkiV"
        return feedback_link