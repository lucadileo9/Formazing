"""
NotionDataParser - Parsing e mapping dati Notion

Questo modulo gestisce:
- Parsing di tutti i tipi campo Notion
- Mapping da formato Notion a formato interno
- Validazione e normalizzazione dati
- Gestione robusta di campi malformati
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional


logger = logging.getLogger(__name__)


class NotionDataParser:
    """
    Parser specializzato per conversione dati Notion → formato interno.
    
    RESPONSABILITÀ:
    - Parsing di ogni tipo campo Notion (title, select, multi_select, etc.)
    - Mapping completo pagina Notion → oggetto formazione
    - Validazione dati e gestione errori
    - Normalizzazione formati (date, testi, URL)
    """
    
    def __init__(self):
        """Inizializza data parser."""
        logger.debug("NotionDataParser inizializzato")
    
    def parse_formazioni_list(self, notion_response: Dict) -> List[Dict]:
        """
        Parsa lista completa formazioni da response Notion.
        
        METODO PRINCIPALE per parsing bulk data.
        
        Args:
            notion_response: Response completa da API Notion
        
        Returns:
            List[Dict]: Lista formazioni normalizzate (filtra malformate)
        """
        logger.debug(f"Parsing {len(notion_response.get('results', []))} formazioni da Notion")
        
        formazioni = []
        for page in notion_response.get('results', []):
            formazione = self.parse_single_formazione(page)
            if formazione:  # Filtra righe malformate
                formazioni.append(formazione)
        
        logger.info(f"Parsate {len(formazioni)} formazioni valide")
        return formazioni
    
    def parse_single_formazione(self, page: Dict) -> Optional[Dict]:
        """
        Parsa singola pagina Notion in formazione interna.
        
        MAPPING COMPLETO CAMPI:
        - Nome: page title → Nome (string)
        - Area: multi_select → Area (comma-separated string)
        - Data: date → Data/Ora (dd/mm/YYYY HH:MM)
        - Status: status → Stato/Fase (string)
        - Codice: rich_text → Codice (string)
        - Link Teams: url → Link Teams (string)
        - Periodo: select → Periodo (string)
        
        Args:
            page: Pagina singola da API Notion
        
        Returns:
            Dict: Formazione normalizzata o None se parsing fallisce
        """
        try:
            properties = page.get('properties', {})
            
            # Estrazione campi obbligatori
            nome = self.extract_page_title_property(properties.get('Nome'))
            area = self.extract_multi_select_property(properties.get('Area'))
            data_ora = self.extract_date_property(properties.get('Date'))
            status = self.extract_status_property(properties.get('Stato'))
            
            # Validazione campi critici
            if not all([nome, area, data_ora, status]):
                logger.warning(f"Formazione con campi mancanti: {page.get('id', 'unknown')}")
                return None
            
            # Estrazione campi opzionali
            codice = self.extract_rich_text_property(properties.get('Codice')) or ''
            link_teams = self.extract_url_property(properties.get('Link Teams')) or ''
            periodo = self.extract_select_property(properties.get('Periodo')) or ''
            
            # Costruzione formazione normalizzata
            formazione = {
                'Nome': nome,
                'Area': area,
                'Data/Ora': data_ora,
                'Stato/Fase': status,
                'Codice': codice,
                'Link Teams': link_teams,
                'Periodo': periodo,
                '_notion_id': page.get('id')  # ID interno per updates
            }
            
            logger.debug(f"Formazione parsata: {nome} ({area}) - {data_ora}")
            return formazione
            
        except Exception as e:
            logger.error(f"Errore parsing formazione {page.get('id', 'unknown')}: {e}")
            return None
    
    # ===============================
    # PARSING TIPI CAMPO SPECIFICI
    # ===============================
    
    def extract_page_title_property(self, title_prop: Dict) -> str:
        """
        Estrae titolo da property Title di Notion.
        
        Struttura Notion:
        {"title": [{"plain_text": "Titolo Formazione"}]}
        """
        if not title_prop or not title_prop.get('title'):
            return ''
        return ''.join([t.get('plain_text', '') for t in title_prop['title']])
    
    def extract_select_property(self, select_prop: Dict) -> str:
        """
        Estrae valore da property Select di Notion.
        
        Struttura Notion:
        {"select": {"name": "SPRING", "color": "blue"}}
        """
        if not select_prop or not select_prop.get('select'):
            return ''
        return select_prop['select'].get('name', '')
    
    def extract_multi_select_property(self, multi_select_prop: Dict) -> str:
        """
        Estrae valori da property Multi-Select di Notion.
        
        Struttura Notion:
        {"multi_select": [{"name": "IT"}, {"name": "R&D"}]}
        
        Output: "IT, R&D"
        """
        if not multi_select_prop or not multi_select_prop.get('multi_select'):
            return ''
        
        values = [item.get('name', '') for item in multi_select_prop['multi_select']]
        return ', '.join(filter(None, values))  # Filtra valori vuoti
    
    def extract_status_property(self, status_prop: Dict) -> str:
        """
        Estrae valore da property Status di Notion.
        
        Struttura Notion:
        {"status": {"name": "Programmata", "color": "blue"}}
        """
        if not status_prop or not status_prop.get('status'):
            return ''
        return status_prop['status'].get('name', '')
    
    def extract_rich_text_property(self, rich_text_prop: Dict) -> str:
        """
        Estrae testo da property Rich Text di Notion.
        
        Strutura Notion:
        {"rich_text": [{"plain_text": "Testo contenuto"}]}
        """
        if not rich_text_prop or not rich_text_prop.get('rich_text'):
            return ''
        return ''.join([t.get('plain_text', '') for t in rich_text_prop['rich_text']])
    
    def extract_url_property(self, url_prop: Dict) -> str:
        """
        Estrae URL da property URL di Notion.
        
        Struttura Notion:
        {"url": "https://teams.microsoft.com/..."}
        """
        if not url_prop:
            return ''
        return url_prop.get('url', '') or ''
    
    def extract_date_property(self, date_prop: Dict) -> str:
        """
        Estrae e normalizza data da property Date di Notion.
        
        CONVERSIONE FORMATI:
        - Input: ISO (2024-03-15T14:00:00.000Z)
        - Output: dd/mm/YYYY HH:MM (15/03/2024 14:00)
        
        Gestisce:
        - Date con timezone UTC
        - Date senza orario (→ 09:00 default)
        - Date malformate (→ fallback stringa originale)
        
        Args:
            date_prop: Property Date da API Notion
        
        Returns:
            str: Data formattata o stringa vuota
        """
        if not date_prop or not date_prop.get('date'):
            return ''
        
        date_obj = date_prop['date']
        start_date = date_obj.get('start')
        
        if not start_date:
            return ''
        
        try:
            # Parsing data ISO da Notion
            if 'T' in start_date:
                # Formato completo con orario
                dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            else:
                # Solo data, aggiungi orario default
                dt = datetime.fromisoformat(start_date + 'T09:00:00')
            
            # Formattazione output standard
            formatted_date = dt.strftime('%d/%m/%Y %H:%M')
            logger.debug(f"Data convertita: {start_date} → {formatted_date}")
            return formatted_date
            
        except Exception as e:
            logger.warning(f"Errore parsing data '{start_date}': {e}")
            return start_date  # Fallback a stringa originale