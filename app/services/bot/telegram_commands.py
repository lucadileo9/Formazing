"""
Telegram Commands - Gestione comandi bot interattivi

Questo modulo gestisce:
- Comandi bot: /oggi, /domani, /settimana, /help, /start
- Recupero dati formazioni da Notion
- Formattazione risposte HTML per utenti
- Utility per parsing date e ordinamento
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from telegram.ext import CommandHandler, ContextTypes
from telegram import Update

logger = logging.getLogger(__name__)


class TelegramCommands:
    """
    Gestisce tutti i comandi bot interattivi.
    
    RESPONSABILITÀ:
    - Registrazione command handlers
    - Implementazione comandi /oggi, /domani, /settimana, /help
    - Recupero dati formazioni tramite notion_service
    - Formattazione risposte user-friendly
    """
    
    def __init__(self, telegram_service):
        """
        Inizializza gestore comandi con riferimento al servizio principale.
        
        Args:
            telegram_service: Istanza TelegramService per accesso a gruppi e bot
        """
        self.service = telegram_service
        self.notion_service = None  # Configurato da TelegramService.__init__ tramite self.commands.notion_service
        logger.debug("TelegramCommands inizializzato")
    
    def register_handlers(self, application):
        """
        Registra tutti i command handlers nell'applicazione Telegram.
        
        COMANDI REGISTRATI:
        - /oggi: formazioni di oggi
        - /domani: formazioni di domani  
        - /settimana: formazioni della settimana corrente
        - /help, /start: informazioni sui comandi disponibili
        
        Args:
            application: Istanza Application Telegram per registrazione handlers
        """
        application.add_handler(CommandHandler("oggi", self.command_oggi))
        application.add_handler(CommandHandler("domani", self.command_domani))
        application.add_handler(CommandHandler("settimana", self.command_settimana))
        application.add_handler(CommandHandler("help", self.command_help))
        application.add_handler(CommandHandler("start", self.command_help))  # Alias
        
        logger.info("✅ Command handlers registrati: /oggi, /domani, /settimana, /help, /start")
    
    # ===============================
    # COMANDI BOT PUBBLICI
    # ===============================
    
    async def command_oggi(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Comando /oggi - Mostra formazioni calendarizzate per oggi.
        
        FUNZIONALITÀ:
        - Recupera formazioni con status 'Calendarizzata' per data odierna
        - Ordina per orario di inizio
        - Formatta risposta HTML con dettagli completi
        """
        await self._handle_date_command(update, context, days_offset=0, period_name="oggi")
    
    async def command_domani(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Comando /domani - Mostra formazioni calendarizzate per domani.
        
        FUNZIONALITÀ:
        - Identico a /oggi ma per data = oggi + 1 giorno
        - Utile per pianificazione e promemoria
        """
        await self._handle_date_command(update, context, days_offset=1, period_name="domani")
    
    async def command_settimana(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Comando /settimana - Mostra tutte le formazioni della settimana (Lun-Dom).
        
        FUNZIONALITÀ AVANZATE:
        - Calcola automaticamente range settimana corrente
        - Raggruppa formazioni per giorno
        - Mostra nomi giorni in italiano
        - Formattazione gerarchica giorno > formazioni
        """
        if self.notion_service is None:
            await update.message.reply_text("❌ Servizio non disponibile al momento")
            return
        
        try:
            # Calcolo range settimana corrente (Lunedì-Domenica)
            today = datetime.now().date()
            start_of_week = today - timedelta(days=today.weekday())  # Lunedì = 0
            end_of_week = start_of_week + timedelta(days=6)  # Domenica
            
            # Recupero formazioni nel range settimanale
            formazioni = await self._get_formazioni_by_date_range(start_of_week, end_of_week)
            
            # Header risposta con date range
            message = f"📅 <b>FORMAZIONI SETTIMANA</b> ({start_of_week.strftime('%d/%m')} - {end_of_week.strftime('%d/%m/%Y')}):\n\n"
            
            if not formazioni:
                message += "🤷‍♂️ <i>Nessuna formazione in programma questa settimana</i>"
            else:
                # Raggruppamento formazioni per giorno
                formazioni_per_giorno = {}
                for formazione in formazioni:
                    data_str = self._extract_date_from_formazione(formazione)
                    if data_str:
                        if data_str not in formazioni_per_giorno:
                            formazioni_per_giorno[data_str] = []
                        formazioni_per_giorno[data_str].append(formazione)
                
                # Ordinamento e formattazione per giorno
                for data in sorted(formazioni_per_giorno.keys()):
                    day_name = self._get_day_name(data)
                    message += f"📆 <b>{day_name} {data}</b>:\n"
                    
                    # Formazioni del giorno ordinate per ora
                    for formazione in formazioni_per_giorno[data]:
                        # Formattazione Area: lista → stringa pulita
                        area_raw = formazione.get('Area', 'N/A')
                        if isinstance(area_raw, list) and area_raw:
                            area = ', '.join(area_raw)
                        else:
                            area = area_raw if area_raw else 'N/A'
                        
                        nome = formazione.get('Nome', 'N/A')
                        ora = self._extract_time_from_formazione(formazione)
                        codice = formazione.get('Codice', '')
                        link_teams = formazione.get('Link Teams', '')
                        
                        message += f"  • <b>{area}</b> - {nome} (<b>{ora}</b>)\n"
                        if codice:
                            message += f"    🏷 <code>{codice}</code>\n"
                        if link_teams:
                            message += f"    🔗 <a href='{link_teams}'>Link Teams</a>\n"
                    message += "\n"
            
            await update.message.reply_text(message, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Errore nel comando /settimana: {e}")
            await update.message.reply_text("❌ Errore nel recupero delle formazioni della settimana")
    
    async def command_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Comando /help e /start - Mostra guida comandi disponibili.
        
        CONTENUTO:
        - Lista comandi con descrizioni
        - Informazioni sui dati mostrati
        - Note sui requisiti (formazioni calendarizzate)
        """
        help_text = """🤖 <b>Bot Formazing - Comandi Disponibili</b>

📅 <b>/oggi</b> - Mostra le formazioni di oggi
📅 <b>/domani</b> - Mostra le formazioni di domani  
📅 <b>/settimana</b> - Mostra tutte le formazioni della settimana
❓ <b>/help</b> - Mostra questo messaggio

💡 <i>Tutti i comandi mostrano solo le formazioni già calendarizzate con link Teams attivi!</i>

🔗 <b>Informazioni per ogni formazione:</b>
• Area di competenza
• Nome della formazione
• Data e ora
• Codice identificativo
• Link Teams (quando disponibile)"""

        await update.message.reply_text(help_text, parse_mode='HTML')
    
    # ===============================
    # METODI UTILITY INTERNI
    # ===============================
    
    async def _handle_date_command(self, update, context, days_offset: int, period_name: str):
        """
        Gestisce logica comune per comandi /oggi e /domani.
        
        PROCESSO:
        1. Valida disponibilità notion_service
        2. Calcola data target (oggi + offset)
        3. Recupera formazioni filtrate per data
        4. Formatta risposta ordinata per ora
        5. Invia messaggio HTML all'utente
        
        Args:
            update: Update Telegram
            context: Contesto comando
            days_offset (int): Giorni da oggi (0=oggi, 1=domani)
            period_name (str): Nome periodo per messaggi
        """
        if self.notion_service is None:
            await update.message.reply_text("❌ Servizio non disponibile al momento")
            return
        
        try:
            # Calcolo data target
            target_date = datetime.now().date() + timedelta(days=days_offset)
            formazioni = await self._get_formazioni_by_date(target_date)
            
            # Header messaggio
            message = f"📅 <b>FORMAZIONI DI {period_name.upper()}</b> ({target_date.strftime('%d/%m/%Y')}):\n\n"
            
            if not formazioni:
                message += f"🤷‍♂️ <i>Nessuna formazione in programma {period_name}</i>"
            else:
                # Lista numerata formazioni ordinate per ora
                for i, formazione in enumerate(formazioni, 1):
                    # Formattazione Area: lista → stringa pulita
                    area_raw = formazione.get('Area', 'N/A')
                    if isinstance(area_raw, list) and area_raw:
                        area = ', '.join(area_raw)
                    else:
                        area = area_raw if area_raw else 'N/A'
                    
                    nome = formazione.get('Nome', 'N/A')
                    ora = self._extract_time_from_formazione(formazione)
                    codice = formazione.get('Codice', '')
                    link_teams = formazione.get('Link Teams', '')
                    
                    message += f"<b>{i}.</b> <b>{area}</b> - {nome} (<b>{ora}</b>)\n"
                    if codice:
                        message += f"    🏷 Codice: <code>{codice}</code>\n"
                    if link_teams:
                        message += f"    🔗 <a href='{link_teams}'>Link Teams</a>\n"
                    message += "\n"
            
            await update.message.reply_text(message, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Errore nel comando /{period_name}: {e}")
            await update.message.reply_text(f"❌ Errore nel recupero delle formazioni di {period_name}")
    
    # ===============================
    # UTILITY RECUPERO DATI
    # ===============================
    
    async def _get_formazioni_by_date(self, target_date) -> List[Dict]:
        """
        Recupera formazioni calendarizzate per data specifica.
        
        PROCESSO:
        1. Recupera tutte le formazioni 'Calendarizzate' da Notion
        2. Filtra per target_date
        3. Ordina per orario crescente
        
        Args:
            target_date (date): Data specifica per filtraggio
            
        Returns:
            List[Dict]: Formazioni ordinate per ora
        """
        if self.notion_service is None:
            return []
        
        try:
            # Recupero tutte le formazioni calendarizzate
            all_formazioni = await self.notion_service.get_formazioni_by_status('Calendarizzata')
            
            # Filtraggio per data target
            formazioni_del_giorno = []
            for formazione in all_formazioni:
                formazione_date = self._extract_date_from_formazione(formazione)
                if formazione_date and formazione_date == target_date.strftime('%d/%m/%Y'):
                    formazioni_del_giorno.append(formazione)
            
            # Ordinamento per orario
            sorted_formazioni = sorted(formazioni_del_giorno, key=lambda x: self._extract_time_from_formazione(x))
            
            logger.info(f"Recuperate {len(sorted_formazioni)} formazioni per {target_date.strftime('%d/%m/%Y')}")
            return sorted_formazioni
            
        except Exception as e:
            logger.error(f"Errore nel recupero formazioni per data {target_date}: {e}")
            return []
    
    async def _get_formazioni_by_date_range(self, start_date, end_date) -> List[Dict]:
        """
        Recupera formazioni calendarizzate in range di date per /settimana.
        
        Args:
            start_date (date): Data inizio range (inclusa)
            end_date (date): Data fine range (inclusa)
            
        Returns:
            List[Dict]: Formazioni nel range (non ordinate)
        """
        if self.notion_service is None:
            return []
        
        try:
            # Recupero base da Notion
            all_formazioni = await self.notion_service.get_formazioni_by_status('Calendarizzata')
            
            # Filtraggio per range di date
            formazioni_periodo = []
            for formazione in all_formazioni:
                formazione_date_str = self._extract_date_from_formazione(formazione)
                if formazione_date_str:
                    try:
                        formazione_date = datetime.strptime(formazione_date_str, '%d/%m/%Y').date()
                        if start_date <= formazione_date <= end_date:
                            formazioni_periodo.append(formazione)
                    except ValueError:
                        logger.warning(f"Data non parsabile: {formazione_date_str}")
                        continue
            
            logger.info(f"Recuperate {len(formazioni_periodo)} formazioni per range {start_date}-{end_date}")
            return formazioni_periodo
            
        except Exception as e:
            logger.error(f"Errore nel recupero formazioni per range {start_date}-{end_date}: {e}")
            return []
    
    # ===============================
    # UTILITY PARSING DATE
    # ===============================
    
    def _extract_date_from_formazione(self, formazione: Dict) -> Optional[str]:
        """
        Estrae data in formato dd/mm/yyyy da formazione.
        
        FORMATI SUPPORTATI:
        - ISO: "2024-09-22T14:30:00Z" → "22/09/2024"
        - Custom: "22/09/2024 14:30" → "22/09/2024"
        
        Returns:
            Optional[str]: Data "dd/mm/yyyy" o None se parsing fallisce
        """
        try:
            data_ora = formazione.get('Data/Ora')
            if not isinstance(data_ora, str):
                return None
                
            if 'T' in data_ora:  # ISO format
                dt = datetime.fromisoformat(data_ora.replace('Z', '+00:00'))
                return dt.strftime('%d/%m/%Y')
            else:  # Custom format  
                dt = datetime.strptime(data_ora, '%d/%m/%Y %H:%M')
                return dt.strftime('%d/%m/%Y')
                
        except Exception:
            return None
    
    def _extract_time_from_formazione(self, formazione: Dict) -> str:
        """
        Estrae orario in formato HH:MM da formazione.
        
        Returns:
            str: Orario "HH:MM" o "N/A" se estrazione fallisce
        """
        try:
            data_ora = formazione.get('Data/Ora')
            if not isinstance(data_ora, str):
                return 'N/A'
                
            if 'T' in data_ora:  # ISO format
                dt = datetime.fromisoformat(data_ora.replace('Z', '+00:00'))
                return dt.strftime('%H:%M')
            else:  # Custom format
                dt = datetime.strptime(data_ora, '%d/%m/%Y %H:%M')
                return dt.strftime('%H:%M')
                
        except Exception:
            return 'N/A'
    
    def _get_day_name(self, date_str: str) -> str:
        """
        Converte data dd/mm/yyyy in nome giorno italiano.
        
        Returns:
            str: Nome giorno ("Lunedì", "Martedì", ...) o "N/A" se errore
        """
        try:
            dt = datetime.strptime(date_str, '%d/%m/%Y')
            days = ['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica']
            return days[dt.weekday()]
        except Exception:
            return 'N/A'