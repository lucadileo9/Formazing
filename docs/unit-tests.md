# Unit Tests - NotionService

Documentazione dei test unitari per i moduli del NotionService.

## Strategia di Testing

- **Framework**: pytest con markers (`@pytest.mark.unit`, `@pytest.mark.notion`)
- **Approccio**: Test per singolo modulo, focus su edge cases e robustezza
- **Performance**: Esecuzione rapida (< 1 secondo per modulo)
- **Coverage**: Tutti i metodi pubblici + gestione errori

## DataParser Tests

**File**: `tests/unit/notion/test_data_parser.py`  
**Modulo**: `app.services.notion.data_parser.NotionDataParser`  
**Test Count**: 30 test | **Runtime**: ~0.21s

### Categorie Test

#### 1. Parsing Completo (6 test)
- ✅ `test_parse_single_formazione_complete` - Formazione con tutti i campi
- ✅ `test_parse_single_formazione_minimal` - Formazione con campi minimi
- ✅ `test_parse_single_formazione_incomplete_returns_none` - Formazione invalida
- ✅ `test_parse_formazioni_list_complete` - Lista completa di formazioni
- ✅ `test_parse_formazioni_list_empty_response` - Response API vuota
- ✅ `test_parse_formazioni_list_filters_incomplete` - Filtro formazioni incomplete

#### 2. Metodi Extract Specifici (12 test)
- ✅ `test_extract_page_title_property_*` (3 test) - Titoli: semplici, multi-part, vuoti
- ✅ `test_extract_multi_select_property_*` (3 test) - Multi-select: singolo, multiplo, vuoto
- ✅ `test_extract_date_property_*` (4 test) - Date: con/senza ora, malformate, null
- ✅ `test_extract_status_property_*` (2 test) - Status: standard, valori diversi

#### 3. Proprietà Avanzate (6 test)
- ✅ `test_extract_rich_text_property_*` (3 test) - Rich text: semplice, complesso, vuoto
- ✅ `test_extract_url_property_*` (2 test) - URL: validi, null
- ✅ `test_extract_select_property_*` (2 test) - Select: normale, vuoto

#### 4. Edge Cases & Robustezza (6 test)
- ✅ `test_parse_single_formazione_missing_properties` - Struttura senza properties
- ✅ `test_parse_single_formazione_invalid_structure` - JSON completamente invalido
- ✅ `test_extract_methods_handle_none_gracefully` - Gestione input None
- ✅ `test_extract_methods_handle_empty_dict_gracefully` - Gestione dict vuoti
- ✅ `test_real_world_parsing_scenario` - Scenario misto realistico

### Fixture Utilizzate
- `sample_notion_page` - Formazione completa standard
- `sample_notion_page_minimal` - Formazione con campi minimi
- `sample_notion_page_incomplete` - Formazione senza campi obbligatori
- `notion_query_response` - Response API completa
- `notion_page_malformed_date` - Pagina con data malformata
- `notion_page_rich_text_complex` - Rich text con formattazione

### Esecuzione
```bash
# Tutti i test DataParser
pytest tests/unit/notion/test_data_parser.py -v

# Solo test DataParser con marker
pytest -m "unit and notion" tests/unit/notion/test_data_parser.py -v
```

---

## Prossimi Moduli

### QueryBuilder (Priorità #2)
- **File**: `tests/unit/notion/test_query_builder.py` (TODO)
- **Focus**: Costruzione query Notion API, filtri, ordinamenti

### CrudOperations (Priorità #3)
- **File**: `tests/unit/notion/test_crud_operations.py` (TODO)
- **Focus**: Create, Update, gestione errori API

### Altri Moduli
- **NotionClient**: Connessione, autenticazione, retry logic
- **Diagnostics**: Health check, validazione configurazione
- **Facade**: Integrazione moduli, workflow completi

---

## Note Tecniche

- **Isolamento**: Ogni test è indipendente, usa fixture dedicate
- **Mocking**: Nessuna chiamata API reale nei unit test
- **Documentazione**: Ogni test ha docstring dettagliata con scopo e verifiche
- **Markers**: `@pytest.mark.unit` e `@pytest.mark.notion` per filtering
- **Performance**: Target < 1s per modulo per feedback rapido durante sviluppo