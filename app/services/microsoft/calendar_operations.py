"""
Calendar Operations - Creazione eventi calendario con Teams meeting.

Gestisce la creazione di eventi nel calendario Microsoft tramite Graph API.
Usa direttamente i nomi dei campi Notion per semplicità.
"""

import logging
import json
from typing import Dict, List
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)


class CalendarOperationsError(Exception):
    """Eccezione per errori nelle operazioni calendario."""
    pass


class CalendarOperations:
    """Gestore operazioni calendario Microsoft."""
    
    def __init__(self, graph_client, email_formatter):
        """
        Inizializza il gestore operazioni calendario.
        
        Args:
            graph_client: Istanza GraphClient per autenticazione
            email_formatter: Istanza EmailFormatter per template
        """
        self.graph_client = graph_client
        self.email_formatter = email_formatter
        self.area_emails = self._load_area_emails()
        
        logger.info("CalendarOperations initialized")
    
    def _load_area_emails(self) -> Dict[str, str]:
        """Carica il mapping Area → Email dal file JSON."""
        try:
            base_path = Path(__file__).parent.parent.parent.parent
            email_config_path = base_path / "config" / "microsoft_emails.json"
            
            with open(email_config_path, 'r', encoding='utf-8') as f:
                area_emails = json.load(f)
            
            logger.debug(f"Loaded {len(area_emails)} area email mappings")
            return area_emails
            
        except FileNotFoundError:
            logger.error(f"Email config file not found: {email_config_path}")
            raise CalendarOperationsError(f"Missing email config: {email_config_path}")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in email config: {e}")
            raise CalendarOperationsError(f"Invalid email config JSON: {e}")
    
    def _convert_notion_date_to_iso(self, date_str: str) -> str:
        """
        Converte data da formato Notion a ISO.
        
        Args:
            date_str: Data in formato 'dd/mm/YYYY HH:MM' o già ISO
            
        Returns:
            Data in formato ISO (YYYY-MM-DDTHH:MM:SSZ)
        """
        try:
            # Se è già ISO, ritorna così
            if 'T' in date_str:
                return date_str if date_str.endswith('Z') else date_str + 'Z'
            
            # Formato Notion: dd/mm/YYYY HH:MM
            if '/' in date_str:
                dt = datetime.strptime(date_str, '%d/%m/%Y %H:%M')
                return dt.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'
            
            raise ValueError(f"Formato data non riconosciuto: {date_str}")
            
        except Exception as e:
            logger.error(f"Errore conversione data '{date_str}': {e}")
            raise CalendarOperationsError(f"Formato data non valido: {date_str}")
    
    def _get_attendee_emails_for_areas(self, areas: List[str]) -> List[str]:
        """
        Ottiene le email delle mailing list per le aree specificate.
        
        Args:
            areas: Lista di aree (es. ["IT", "R&D"])
            
        Returns:
            Lista di email uniche (rimuove duplicati)
        """
        emails = []
        for area in areas:
            email = self.area_emails.get(area, self.area_emails.get('default', 'formazioni@jemore.it'))
            if email not in emails:  # Evita duplicati
                emails.append(email)
        
        logger.debug(f"Attendee emails for areas {areas}: {emails}")
        return emails
    
    def create_calendar_event(self, formazione_data: Dict) -> Dict:
        """
        Crea un evento calendario con Teams meeting per una formazione.
        
        USA DIRETTAMENTE I NOMI DEI CAMPI NOTION (no mapping).
        
        Args:
            formazione_data: Dati formazione da Notion (formato originale)
                {
                    'Nome': 'Sicurezza Informatica',
                    'Codice': 'IT-Security-2024-SPRING-01',
                    'Data/Ora': '15/10/2024 14:30',
                    'Area': ['IT', 'R&D']  # ← Lista di aree!
                }
        
        Returns:
            Dict con risultato creazione:
            {
                'event_id': 'AAMkAGI...',
                'teams_link': 'https://teams.microsoft.com/l/meetup-join/...',
                'calendar_link': 'https://outlook.office365.com/...',
                'subject': 'Sicurezza Informatica',
                'attendee_emails': ['it@jemore.it', 'rd@jemore.it']
            }
        """
        try:
            nome = formazione_data.get('Nome', '')
            codice = formazione_data.get('Codice', '')
            data_ora = formazione_data.get('Data/Ora', '')
            areas = formazione_data.get('Area', [])
            
            logger.info(f"Creating calendar event for: {nome}")
            
            # Validazione campi obbligatori
            if not nome or not data_ora:
                raise CalendarOperationsError("Campi obbligatori mancanti: Nome, Data/Ora")
            
            # Assicurati che Area sia una lista
            if isinstance(areas, str):
                areas = [areas]
            elif not areas:
                areas = ['default']
            
            # 1. Converti data da Notion a ISO
            data_iso = self._convert_notion_date_to_iso(data_ora)
            
            # 2. Calcola data fine (+1 ora)
            start_dt = datetime.fromisoformat(data_iso.replace('Z', '+00:00'))
            end_dt = start_dt + timedelta(hours=1)
            
            start_time = {
                "dateTime": start_dt.strftime("%Y-%m-%dT%H:%M:%S"),
                "timeZone": "Europe/Rome"
            }
            end_time = {
                "dateTime": end_dt.strftime("%Y-%m-%dT%H:%M:%S"),
                "timeZone": "Europe/Rome"
            }
            
            # 3. Ottieni email per tutte le aree
            attendee_emails = self._get_attendee_emails_for_areas(areas)
            
            # 4. Crea lista attendees per Graph API
            attendees = []
            for email in attendee_emails:
                attendees.append({
                    "emailAddress": {
                        "address": email,
                        "name": f"Team {', '.join(areas)}"
                    },
                    "type": "required"
                })
            
            # 5. Prepara subject e body (usa direttamente i campi Notion)
            subject = self.email_formatter.format_subject(formazione_data)
            body = self.email_formatter.format_calendar_body(formazione_data)
            
            # 6. Costruisci payload Graph API
            event_payload = {
                "subject": subject,
                "body": {
                    "contentType": "HTML",
                    "content": body
                },
                "start": start_time,
                "end": end_time,
                "attendees": attendees,
                "isOnlineMeeting": True,
                "onlineMeetingProvider": "teamsForBusiness"
            }
            
            # 7. Crea evento via Graph API
            user_email = self.graph_client.user_email
            endpoint = f"/users/{user_email}/events"
            
            response = self.graph_client.make_request(
                method="POST",
                endpoint=endpoint,
                json_data=event_payload
            )
            
            logger.info(f"Event created successfully: {response.get('id')}")
            
            # 8. Estrai Teams link direttamente dalla risposta
            teams_link = response.get('onlineMeeting', {}).get('joinUrl')
            
            if not teams_link:
                logger.warning("Teams link not found in response")
            
            # 9. Prepara risultato
            result = {
                'event_id': response.get('id'),
                'teams_link': teams_link,
                'calendar_link': response.get('webLink'),
                'subject': response.get('subject'),
                'start_date': response.get('start', {}).get('dateTime'),
                'attendee_emails': attendee_emails,
                'areas': areas,
                'is_online_meeting': response.get('isOnlineMeeting', False)
            }
            
            logger.info(
                f"Calendar event created: {result['subject']} | "
                f"Teams: {bool(teams_link)} | "
                f"Attendees: {', '.join(attendee_emails)}"
            )
            
            return result
            
        except KeyError as e:
            logger.error(f"Missing required field in formazione_data: {e}")
            raise CalendarOperationsError(f"Campo obbligatorio mancante: {e}")
        except Exception as e:
            logger.error(f"Calendar event creation failed: {e}")
            raise CalendarOperationsError(f"Errore creazione evento: {str(e)}")
