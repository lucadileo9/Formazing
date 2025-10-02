"""
Unit test per NotionDataParser.

Testa parsing e conversione dati da formato Notion API a formato interno.
Focus su:
- Parsing completo formazioni
- Gestione campi mancanti/malformati
- Conversione date ISO → italiano
- Estrazione multi-select, rich text, status
- Edge cases e validazioni

UTILIZZO:
pytest tests/unit/notion/test_data_parser.py -v
pytest -m "unit and notion" -v
"""

import pytest
from datetime import datetime
from app.services.notion.data_parser import NotionDataParser


@pytest.mark.unit
@pytest.mark.notion
class TestNotionDataParser:
    """Test suite per NotionDataParser."""
    
    @pytest.fixture
    def parser(self):
        """Istanza NotionDataParser per test."""
        return NotionDataParser()
    
    # ===== TEST PARSING COMPLETO =====
    
    def test_parse_single_formazione_complete(self, parser, sample_notion_page):
        """
        Test parsing di una formazione completa con tutti i campi popolati.
        
        Verifica che:
        - Tutti i campi vengano estratti correttamente
        - I tipi di dato siano preservati (string, URL, etc.)
        - Il mapping Nome → 'Nome', Area → 'Area', etc. funzioni
        - Il campo _notion_id venga aggiunto per tracking interno
        
        Questo è il caso d'uso principale del parser.
        """
        result = parser.parse_single_formazione(sample_notion_page)
        
        # Verifiche generali
        assert result is not None
        assert isinstance(result, dict)
        assert '_notion_id' in result
        
        # Verifiche campi specifici
        assert result['Nome'] == "Sicurezza Web Avanzata"
        assert result['Area'] == "IT, R&D"
        assert result['Data/Ora'] == "15/03/2024 14:00"
        assert result['Stato'] == "Programmata"
        assert result['Codice'] == "IT-Sicurezza-2024-SPRING-01"
        assert result['Link Teams'] == "https://teams.microsoft.com/l/meetup-join/abc123"
        assert result['Periodo'] == "SPRING"
        assert result['_notion_id'] == "abc123-def456-ghi789"
    
    def test_parse_single_formazione_minimal(self, parser, sample_notion_page_minimal):
        """
        Test parsing di formazione con solo campi obbligatori compilati.
        
        Verifica che:
        - Campi obbligatori (Nome, Area, Date, Stato) vengano estratti
        - Campi opzionali vuoti non causino errori
        - Campi opzionali vuoti vengano impostati a stringa vuota
        
        Importante per gestire formazioni in fase di compilazione
        o database con dati parziali.
        """
        result = parser.parse_single_formazione(sample_notion_page_minimal)
        
        assert result is not None
        
        # Campi obbligatori presenti
        assert result['Nome'] == "Test Formazione Minimale"
        assert result['Area'] == "IT"
        assert result['Data/Ora'] == "20/03/2024 09:00"
        assert result['Stato'] == "Calendarizzata"
        
        # Campi opzionali vuoti ma presenti
        assert result['Codice'] == ""
        assert result['Link Teams'] == ""
        assert result['Periodo'] == ""
        
        assert result['_notion_id'] == "minimal-test-id"
    
    def test_parse_single_formazione_incomplete_returns_none(self, parser, sample_notion_page_incomplete):
        """
        Test parsing di formazione con campi obbligatori mancanti.
        
        Verifica che:
        - Formazioni incomplete vengano scartate (return None)
        - Il sistema non crasha con dati malformati
        - La validazione dei campi critici funzioni correttamente
        
        Essenziale per robustezza: meglio scartare una formazione
        che far crashare tutto il sistema con dati incompleti.
        """
        result = parser.parse_single_formazione(sample_notion_page_incomplete)
        
        # Formazione incompleta deve essere scartata
        assert result is None
    
    def test_parse_formazioni_list_complete(self, parser, notion_query_response):
        """
        Test parsing di lista formazioni da response API reale.
        
        Verifica che:
        - Array di formazioni venga processato correttamente
        - Ogni formazione mantenga i propri dati distinti
        - Il parsing di massa non introduca errori di concorrenza
        
        Simula il caso d'uso più comune: query API che ritorna
        multiple formazioni da dashboard o comandi bot.
        """
        result = parser.parse_formazioni_list(notion_query_response)
        
        assert isinstance(result, list)
        assert len(result) == 2  # Due formazioni nel mock
        
        # Prima formazione
        first = result[0]
        assert first['Nome'] == "Sicurezza Web Avanzata"
        assert first['Area'] == "IT, R&D"
        
        # Seconda formazione
        second = result[1]
        assert second['Nome'] == "Marketing Digital Strategy"
        assert second['Area'] == "Marketing"
        assert second['Stato'] == "Conclusa"
    
    def test_parse_formazioni_list_empty_response(self, parser):
        """
        Test parsing con response API vuota (nessuna formazione trovata).
        
        Verifica che:
        - Response vuota non causi errori
        - Ritorna lista vuota (non None)
        - Gestisce correttamente il caso "nessun risultato"
        
        Importante per query che non trovano match (es: status inesistente,
        date range senza formazioni, etc.).
        """
        empty_response = {"results": [], "has_more": False}
        result = parser.parse_formazioni_list(empty_response)
        
        assert isinstance(result, list)
        assert len(result) == 0
    
    def test_parse_formazioni_list_filters_incomplete(self, parser, sample_notion_page_incomplete):
        """
        Test che formazioni incomplete vengano filtrate automaticamente.
        
        Verifica che:
        - Lista finale contenga solo formazioni valide
        - Formazioni incomplete vengano scartate silenziosamente
        - Nessun log di errore per formazioni malformate
        
        Garantisce che il sistema sia resiliente a dati sporchi
        nel database senza compromettere le formazioni valide.
        """
        response_with_incomplete = {
            "results": [sample_notion_page_incomplete],
            "has_more": False
        }
        
        result = parser.parse_formazioni_list(response_with_incomplete)
        
        # Lista vuota perché formazione incompleta filtrata
        assert isinstance(result, list)
        assert len(result) == 0
    
    # ===== TEST METODI EXTRACT SPECIFICI =====
    
    def test_extract_page_title_property_simple(self, parser):
        """
        Test estrazione titolo Notion semplice (caso base).
        
        Verifica che:
        - Campo 'title' Notion → stringa semplice
        - Nessuna perdita di testo durante estrazione
        - Funzionamento con titoli standard
        
        Caso d'uso: maggior parte dei titoli formazione.
        """
        title_prop = {"title": [{"plain_text": "Test Formazione"}]}
        result = parser.extract_page_title_property(title_prop)
        
        assert result == "Test Formazione"
    
    def test_extract_page_title_property_multi_part(self, parser, notion_page_rich_text_complex):
        """
        Test estrazione titolo multi-parte con rich text.
        
        Verifica che:
        - Multipli text objects vengano concatenati correttamente
        - Formattazione rich text venga rimossa (bold, italic, etc.)
        - Risultato finale sia stringa pulita
        
        Importante quando utenti usano formattazione nei titoli Notion.
        """
        title_prop = notion_page_rich_text_complex["properties"]["Nome"]
        result = parser.extract_page_title_property(title_prop)
        
        # Dovrebbe concatenare le parti
        assert result == "Formazione Multi-parte"
    
    def test_extract_page_title_property_empty(self, parser):
        """
        Test estrazione titolo vuoto (edge case).
        
        Verifica che:
        - Titolo vuoto non causi crash
        - Ritorna stringa vuota (non None)
        - Gestisce gracefully pagine senza nome
        
        Edge case raro ma possibile se utente crea pagina
        senza titolo in Notion.
        """
        title_prop = {"title": []}
        result = parser.extract_page_title_property(title_prop)
        
        assert result == ""
    
    def test_extract_multi_select_property_single(self, parser):
        """
        Test estrazione multi-select con singolo valore.
        
        Verifica che:
        - Singola area (es: "IT") venga estratta correttamente
        - Nessuna virgola extra nel risultato
        - Funzionamento base multi-select
        
        Caso comune: formazioni specifiche per una sola area.
        """
        multi_select_prop = {"multi_select": [{"name": "IT"}]}
        result = parser.extract_multi_select_property(multi_select_prop)
        
        assert result == "IT"
    
    def test_extract_multi_select_property_multiple(self, parser, notion_page_rich_text_complex):
        """
        Test estrazione multi-select con valori multipli.
        
        Verifica che:
        - Multipli valori vengano uniti con virgola
        - Ordine dei valori sia preservato
        - Join string sia "R&D, IT, HR" (no spazi extra)
        
        Caso importante: formazioni trasversali che riguardano
        multiple aree aziendali.
        """
        area_prop = notion_page_rich_text_complex["properties"]["Area"]
        result = parser.extract_multi_select_property(area_prop)
        
        # Dovrebbe joinare con virgola
        assert result == "R&D, IT, HR"
    
    def test_extract_multi_select_property_empty(self, parser):
        """
        Test estrazione multi-select vuoto.
        
        Verifica che:
        - Multi-select vuoto → stringa vuota
        - Nessun crash con array vuoto
        - Comportamento coerente con altri campi vuoti
        
        Edge case: formazione senza area specificata
        (dovrebbe essere validazione error, ma parser deve gestire).
        """
        multi_select_prop = {"multi_select": []}
        result = parser.extract_multi_select_property(multi_select_prop)
        
        assert result == ""
    
    def test_extract_date_property_with_time(self, parser):
        """
        Test parsing data ISO completa con orario.
        
        Verifica che:
        - Formato ISO (2024-03-15T14:30:00.000Z) → formato italiano (15/03/2024 14:30)
        - Conversione timezone UTC → locale
        - Orario preservato accuratamente
        
        Caso standard: formazioni con data/ora precisa programmata.
        """
        date_prop = {"date": {"start": "2024-03-15T14:30:00.000Z"}}
        result = parser.extract_date_property(date_prop)
        
        assert result == "15/03/2024 14:30"
    
    def test_extract_date_property_without_time(self, parser):
        """
        Test parsing data senza orario specificato.
        
        Verifica che:
        - Data senza tempo → aggiunge orario default (09:00)
        - Comportamento coerente per formazioni "tutto il giorno"
        - Formato output rimane dd/mm/YYYY HH:MM
        
        Caso comune: quando si inserisce solo la data in Notion
        senza specificare l'orario.
        """
        date_prop = {"date": {"start": "2024-03-15"}}
        result = parser.extract_date_property(date_prop)
        
        # Dovrebbe aggiungere orario default 09:00
        assert result == "15/03/2024 09:00"
    
    def test_extract_date_property_malformed(self, parser, notion_page_malformed_date):
        """
        Test parsing data con formato invalido (fallback graceful).
        
        Verifica che:
        - Data malformata non causi crash del parser
        - Ritorna stringa originale come fallback sicuro
        - Sistema rimane operativo anche con dati sporchi
        
        Importante per robustezza: se qualcuno inserisce manualmente
        date in formato sbagliato, sistema non deve crashare.
        """
        date_prop = notion_page_malformed_date["properties"]["Date"]
        result = parser.extract_date_property(date_prop)
        
        # Dovrebbe ritornare stringa originale come fallback
        assert result == "invalid-date-format"
    
    def test_extract_date_property_none(self, parser):
        """
        Test parsing data None/null.
        
        Verifica che:
        - Campo data None → stringa vuota
        - Nessun crash con valore null
        - Comportamento coerente con validazione upstream
        
        Edge case: data non impostata o cancellata in Notion.
        """
        date_prop = {"date": None}
        result = parser.extract_date_property(date_prop)
        
        assert result == ""
    
    def test_extract_status_property_normal(self, parser, sample_notion_page):
        """
        Test estrazione status standard.
        
        Verifica che:
        - Campo status Notion → stringa status
        - Informazioni colore vengano ignorate (solo il nome)
        - Estrazione pulita senza metadati extra
        
        Caso base: tutti gli status standard (Programmata, Calendarizzata, Conclusa).
        """
        status_prop = sample_notion_page["properties"]["Stato"]
        result = parser.extract_status_property(status_prop)
        
        assert result == "Programmata"
    
    def test_extract_status_property_different_values(self, parser):
        """
        Test estrazione status con tutti i valori possibili.
        
        Verifica che:
        - Tutti gli status workflow vengano estratti correttamente
        - Colori diversi non influenzino l'estrazione
        - Consistenza tra status diversi
        
        Importante per workflow completo: Programmata → Calendarizzata → Conclusa.
        """
        status_prop_cal = {"status": {"name": "Calendarizzata", "color": "green"}}
        status_prop_con = {"status": {"name": "Conclusa", "color": "red"}}
        
        assert parser.extract_status_property(status_prop_cal) == "Calendarizzata"
        assert parser.extract_status_property(status_prop_con) == "Conclusa"
    
    def test_extract_rich_text_property_simple(self, parser, sample_notion_page):
        """
        Test estrazione rich text semplice (codice formazione).
        
        Verifica che:
        - Rich text semplice → stringa pulita
        - Nessuna perdita di contenuto
        - Funzionamento con codici standard
        
        Caso comune: codici formazione generati automaticamente
        (es: IT-Sicurezza-2024-SPRING-01).
        """
        codice_prop = sample_notion_page["properties"]["Codice"]
        result = parser.extract_rich_text_property(codice_prop)
        
        assert result == "IT-Sicurezza-2024-SPRING-01"
    
    def test_extract_rich_text_property_multi_part(self, parser, notion_page_rich_text_complex):
        """
        Test estrazione rich text complesso con formattazione.
        
        Verifica che:
        - Multipli text objects vengano concatenati
        - Formattazione (bold, code, etc.) venga rimossa
        - Risultato finale sia stringa semplice
        
        Caso avanzato: quando utenti inseriscono formattazione
        nei campi Codice o altre note.
        """
        codice_prop = notion_page_rich_text_complex["properties"]["Codice"]
        result = parser.extract_rich_text_property(codice_prop)
        
        # Dovrebbe concatenare le parti
        assert result == "COMP-MULTI-2024"
    
    def test_extract_rich_text_property_empty(self, parser, sample_notion_page_minimal):
        """
        Test estrazione rich text vuoto.
        
        Verifica che:
        - Campo vuoto → stringa vuota
        - Nessun crash con array vuoto
        - Comportamento coerente con campi opzionali
        
        Caso comune: formazioni nuove senza codice ancora assegnato.
        """
        codice_prop = sample_notion_page_minimal["properties"]["Codice"]
        result = parser.extract_rich_text_property(codice_prop)
        
        assert result == ""
    
    def test_extract_url_property_normal(self, parser, sample_notion_page):
        """
        Test estrazione URL standard (link Teams).
        
        Verifica che:
        - URL valido venga estratto correttamente
        - Nessuna modifica o encoding dell'URL
        - Preservazione completa del link
        
        Caso principale: link Teams generati automaticamente
        durante calendarizzazione formazione.
        """
        url_prop = sample_notion_page["properties"]["Link Teams"]
        result = parser.extract_url_property(url_prop)
        
        assert result == "https://teams.microsoft.com/l/meetup-join/abc123"
    
    def test_extract_url_property_none(self, parser, sample_notion_page_minimal):
        """
        Test estrazione URL None/vuoto.
        
        Verifica che:
        - URL None → stringa vuota
        - Nessun crash con valore null
        - Comportamento coerente con campi opzionali
        
        Caso comune: formazioni in stato "Programmata" che non hanno
        ancora il link Teams generato.
        """
        url_prop = sample_notion_page_minimal["properties"]["Link Teams"]
        result = parser.extract_url_property(url_prop)
        
        assert result == ""
    
    def test_extract_select_property_normal(self, parser, sample_notion_page):
        """
        Test estrazione select standard (periodo formazione).
        
        Verifica che:
        - Valore select → stringa semplice
        - Metadati colore/tipo vengano ignorati
        - Estrazione pulita del valore
        
        Caso base: periodi SPRING, AUTUMN, ONCE, EXT, OUT.
        """
        select_prop = sample_notion_page["properties"]["Periodo"]
        result = parser.extract_select_property(select_prop)
        
        assert result == "SPRING"
    
    def test_extract_select_property_none(self, parser, sample_notion_page_minimal):
        """
        Test estrazione select None/vuoto.
        
        Verifica che:
        - Select None → stringa vuota
        - Nessun crash con valore null
        - Comportamento coerente con campi opzionali
        
        Edge case: periodo non specificato o cancellato.
        """
        select_prop = sample_notion_page_minimal["properties"]["Periodo"]
        result = parser.extract_select_property(select_prop)
        
        assert result == ""
    
    # ===== TEST EDGE CASES E ROBUSTEZZA =====
    
    def test_parse_single_formazione_missing_properties(self, parser):
        """
        Test parsing con struttura Notion completamente mancante.
        
        Verifica che:
        - Pagina senza "properties" → return None
        - Nessun crash con struttura malformata
        - Graceful degradation per dati corrotti
        
        Edge case estremo: corruzione dati API o bug temporaneo Notion.
        """
        page_no_props = {"id": "test-id"}  # Nessun "properties"
        result = parser.parse_single_formazione(page_no_props)
        
        assert result is None
    
    def test_parse_single_formazione_invalid_structure(self, parser):
        """
        Test parsing con struttura JSON completamente invalida.
        
        Verifica che:
        - JSON invalido → return None
        - Nessun crash del parser
        - Sistema rimane operativo
        
        Protezione contro dati completamente corrotti o
        response API malformate.
        """
        invalid_page = {"invalid": "structure"}
        result = parser.parse_single_formazione(invalid_page)
        
        assert result is None
    
    def test_extract_methods_handle_none_gracefully(self, parser):
        """Test che metodi extract gestiscono None senza crash."""
        assert parser.extract_page_title_property(None) == ""
        assert parser.extract_multi_select_property(None) == ""
        assert parser.extract_date_property(None) == ""
        assert parser.extract_status_property(None) == ""
        assert parser.extract_rich_text_property(None) == ""
        assert parser.extract_url_property(None) == ""
        assert parser.extract_select_property(None) == ""
    
    def test_extract_methods_handle_empty_dict_gracefully(self, parser):
        """
        Test gestione dict vuoti per tutti i metodi extract.
        
        Verifica che:
        - Dict vuoti {} → return ""
        - Nessun KeyError per chiavi mancanti
        - Comportamento coerente tra tutti i metodi
        
        Scenario comune: proprietà Notion con struttura presente
        ma valori interni mancanti o vuoti.
        """
        empty_dict = {}
        
        assert parser.extract_page_title_property(empty_dict) == ""
        assert parser.extract_multi_select_property(empty_dict) == ""
        assert parser.extract_date_property(empty_dict) == ""
        assert parser.extract_status_property(empty_dict) == ""
        assert parser.extract_rich_text_property(empty_dict) == ""
        assert parser.extract_url_property(empty_dict) == ""
        assert parser.extract_select_property(empty_dict) == ""
    
    # ===== TEST INTEGRAZIONE CON FIXTURE REALISTICHE =====
    
    def test_real_world_parsing_scenario(self, parser):
        """
        Test scenario real-world con dati misti completi e incompleti.
        
        Verifica che:
        - Mix di dati completi e incompleti → parsing corretto
        - Robustezza con dataset eterogeneo
        - Nessuna perdita di informazioni valide
        
        Scenario operativo: database Notion con formazioni a stadi diversi
        (nuove senza codice, programmate, calendarizzate, concluse).
        """
        mixed_response = {
            "results": [
                # Formazione completa
                {
                    "id": "complete-id",
                    "properties": {
                        "Nome": {"title": [{"plain_text": "Formazione Completa"}]},
                        "Area": {"multi_select": [{"name": "IT"}]},
                        "Date": {"date": {"start": "2024-04-01T14:00:00.000Z"}},
                        "Stato": {"status": {"name": "Programmata", "color": "blue"}},
                        "Codice": {"rich_text": [{"plain_text": "COMP-2024-01"}]},
                        "Link Teams": {"url": "https://teams.microsoft.com/complete"},
                        "Periodo": {"select": {"name": "SPRING"}}
                    }
                },
                # Formazione minimale
                {
                    "id": "minimal-id",
                    "properties": {
                        "Nome": {"title": [{"plain_text": "Formazione Minimale"}]},
                        "Area": {"multi_select": [{"name": "HR"}]},
                        "Date": {"date": {"start": "2024-04-02"}},
                        "Stato": {"status": {"name": "Calendarizzata", "color": "green"}},
                        "Codice": {"rich_text": []},
                        "Link Teams": {"url": None},
                        "Periodo": {"select": None}
                    }
                },
                # Formazione incompleta (sarà filtrata)
                {
                    "id": "incomplete-id",
                    "properties": {
                        "Nome": {"title": [{"plain_text": "Formazione Incompleta"}]},
                        "Area": {"multi_select": []},  # Area vuota
                        "Date": {"date": None},  # Data mancante
                        "Stato": {"status": {"name": "Programmata", "color": "blue"}}
                    }
                }
            ],
            "has_more": False
        }
        
        result = parser.parse_formazioni_list(mixed_response)
        
        # Solo 2 formazioni valide (quella incompleta filtrata)
        assert len(result) == 2
        
        # Verifica formazione completa
        complete = result[0]
        assert complete['Nome'] == "Formazione Completa"
        assert complete['Codice'] == "COMP-2024-01"
        assert complete['Link Teams'] == "https://teams.microsoft.com/complete"
        
        # Verifica formazione minimale
        minimal = result[1]
        assert minimal['Nome'] == "Formazione Minimale"
        assert minimal['Codice'] == ""
        assert minimal['Link Teams'] == ""
        assert minimal['Data/Ora'] == "02/04/2024 09:00"  # Orario default aggiunto