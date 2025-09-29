# Unit Tests - NotionService

Documentazione dei test unitari per i moduli del NotionService.

## Strategia di Testing

- **Framework**: pytest con markers (`@pytest.mark.unit`, `@pytest.mark.notion`)
- **Approccio**: Test per singolo modulo, focus su edge cases e robustezza
- **Performance**: Esecuzione rapida (< 1 secondo per modulo, 0.82s totale)
- **Coverage**: 4/6 moduli completati - 82 test totali ✅

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

## QueryBuilder Tests

**File**: `tests/unit/notion/test_query_builder.py`  
**Modulo**: `app.services.notion.query_builder.NotionQueryBuilder`  
**Test Count**: 17 test | **Runtime**: ~0.22s

### Categorie Test

#### 1. Status Filter Queries (3 test)
- ✅ `test_build_status_filter_query_programmata` - Query per formazioni programmate
- ✅ `test_build_status_filter_query_calendarizzata` - Query per formazioni calendarizzate  
- ✅ `test_build_status_filter_query_conclusa` - Query per formazioni concluse

#### 2. Date Range Queries (2 test)
- ✅ `test_build_date_range_filter_query_valid_range` - Range date standard
- ✅ `test_build_date_range_filter_query_same_day` - Query per giorno specifico

#### 3. Area Filter Queries (3 test)
- ✅ `test_build_area_filter_query_it` - Filtro per area IT
- ✅ `test_build_area_filter_query_hr` - Filtro per area HR
- ✅ `test_build_area_filter_query_marketing` - Filtro per area Marketing

#### 4. Combined Filter Queries (3 test)
- ✅ `test_build_combined_filter_query_status_only` - Solo status (area None)
- ✅ `test_build_combined_filter_query_status_and_area` - Status + area combinati
- ✅ `test_build_combined_filter_query_different_combinations` - Combinazioni diverse

#### 5. Query Validation (4 test)
- ✅ `test_validate_query_structure_valid_query` - Query valida standard
- ✅ `test_validate_query_structure_missing_database_id` - Query senza database_id
- ✅ `test_validate_query_structure_empty_query` - Query vuota
- ✅ `test_validate_query_structure_minimal_valid_query` - Query minimale valida

#### 6. Edge Cases & Consistency (2 test)
- ✅ `test_query_builder_initialization` - Inizializzazione corretta
- ✅ `test_all_queries_include_date_sorting` - Consistency ordinamento date

### Fixture Utilizzate
- `sample_database_id` - Database ID standard per test
- `expected_status_query` - Query attesa per filtro status
- `expected_date_range_query` - Query attesa per range date
- `expected_area_query` - Query attesa per filtro area
- `expected_combined_query` - Query attesa per filtri combinati
- `invalid_query_samples` - Esempi query invalide

### Esecuzione
```bash
# Tutti i test QueryBuilder
pytest tests/unit/notion/test_query_builder.py -v

# Solo test QueryBuilder con marker
pytest -m "unit and notion" tests/unit/notion/test_query_builder.py -v
```

---

## CrudOperations Tests

**File**: `tests/unit/notion/test_crud_operations.py`  
**Modulo**: `app.services.notion.crud_operations.NotionCrudOperations`  
**Test Count**: 18 test | **Runtime**: ~0.24s

### Categorie Test

#### 1. Update Status Operations (4 test)
- ✅ `test_update_formazione_status_success` - Update status successful
- ✅ `test_update_formazione_status_different_statuses` - Tutti gli status workflow
- ✅ `test_update_formazione_status_api_error` - Gestione APIResponseError
- ✅ `test_update_formazione_status_generic_error` - Gestione errori generici

#### 2. Update Codice e Link Operations (3 test)
- ✅ `test_update_codice_e_link_success` - Update codice + link Teams successful
- ✅ `test_update_codice_e_link_empty_link` - Update solo codice (link vuoto)
- ✅ `test_update_codice_e_link_api_error` - Gestione errori API update

#### 3. Get Formazione Operations (3 test)
- ✅ `test_get_formazione_by_id_success` - Retrieve formazione successful
- ✅ `test_get_formazione_by_id_parse_failure` - Gestione parsing failed
- ✅ `test_get_formazione_by_id_api_error` - Gestione errori API retrieve

#### 4. Multiple Fields Operations (3 test)
- ✅ `test_update_multiple_fields_success` - Update atomico multipli campi
- ✅ `test_update_multiple_fields_partial_update` - Update selettivo campi
- ✅ `test_update_multiple_fields_api_error` - Gestione errori update multiplo

#### 5. Batch Operations (3 test)
- ✅ `test_batch_update_status_all_success` - Batch update tutto successful
- ✅ `test_batch_update_status_partial_failure` - Batch con failures misti
- ✅ `test_batch_update_status_empty_list` - Batch con lista vuota

#### 6. Edge Cases & Initialization (2 test)
- ✅ `test_crud_operations_initialization` - Inizializzazione corretta
- ✅ `test_all_methods_handle_none_gracefully` - Gestione parametri None

### Fixture Utilizzate
- `mock_notion_client` - Mock client Notion per operazioni CRUD
- `sample_notion_id` - ID Notion standard per test
- `sample_update_response` - Response simulata update operations
- `sample_retrieve_response` - Response simulata retrieve operation
- `sample_batch_formazioni_ids` - Lista ID per test batch operations
- `sample_multiple_fields_update` - Dati per test update multipli campi
- `mock_data_parser` - Mock parser per test retrieve operations
- `mock_api_error` - Mock APIResponseError per test gestione errori

### Esecuzione
```bash
# Tutti i test CrudOperations
pytest tests/unit/notion/test_crud_operations.py -v

# Solo test CrudOperations con marker
pytest -m "unit and notion" tests/unit/notion/test_crud_operations.py -v
```

---

## NotionClient Tests

**File**: `tests/unit/notion/test_notion_client.py`  
**Modulo**: `app.services.notion.notion_client.NotionClient`  
**Test Count**: 17 test | **Runtime**: ~0.66s

### Categorie Test

#### 1. Initialization & Credentials (8 test)
- ✅ `test_init_with_explicit_credentials` - Inizializzazione con credenziali esplicite
- ✅ `test_init_with_env_variables` - Inizializzazione da environment variables
- ✅ `test_init_mixed_credentials` - Credenziali miste (explicit + env)
- ✅ `test_init_missing_token_explicit` - Errore token mancante (explicit)
- ✅ `test_init_missing_database_id_explicit` - Errore database_id mancante (explicit)
- ✅ `test_init_missing_token_environment` - Errore token mancante (environment)
- ✅ `test_init_missing_database_id_environment` - Errore database_id mancante (environment)
- ✅ `test_init_empty_environment` - Environment completamente vuoto

#### 2. Client Creation & Error Handling (1 test)
- ✅ `test_init_client_creation_failure` - Gestione fallimento creazione client Notion

#### 3. Public API Methods (3 test)
- ✅ `test_get_client` - Accesso client Notion configurato
- ✅ `test_get_database_id` - Accesso database ID configurato
- ✅ `test_get_config_info_complete` - Informazioni configurazione complete

#### 4. Security & Configuration (2 test)
- ✅ `test_get_config_info_security` - Mascheramento token in output sicuro
- ✅ `test_cache_configuration` - Cache configurazione per ottimizzazioni

#### 5. Edge Cases & Validation (3 test)
- ✅ `test_empty_string_credentials` - Gestione credenziali stringa vuota
- ✅ `test_whitespace_credentials` - Gestione credenziali con solo whitespace
- ✅ `test_notion_client_multiple_instances` - Creazione istanze multiple indipendenti

### Fixture Utilizzate
- `mock_env_empty` - Environment variables vuote per test isolamento
- `mock_env_with_notion_config` - Environment con configurazione Notion
- `mock_notion_client_class` - Mock classe Client Notion ufficiale
- `valid_notion_token` - Token valido standard per test
- `valid_database_id` - Database ID valido standard per test
- `invalid_credentials_scenarios` - Scenari credenziali invalide
- `client_creation_error` - Mock errore creazione client

### Key Features Testate
- **Credential Validation**: Validazione robusta inclusi edge cases (stringhe vuote, whitespace)
- **Environment Precedence**: Logica precedenza parametri espliciti vs environment variables
- **Error Handling**: Gestione completa errori inizializzazione e configurazione
- **Security**: Mascheramento token in output e logging sicuro
- **Multi-Instance**: Supporto istanze multiple indipendenti
- **Cache Strategy**: Configurazione cache per ottimizzazione performance

### Esecuzione
```bash
# Tutti i test NotionClient
pytest tests/unit/notion/test_notion_client.py -v

# Solo test NotionClient con marker
pytest -m "unit and notion" tests/unit/notion/test_notion_client.py -v
```

---

## Prossimi Moduli

### Diagnostics (Priorità #5)
- **File**: `tests/unit/notion/test_diagnostics.py` (TODO)
- **Focus**: Health check, validazione configurazione

### Facade (Priorità #6)
- **File**: `tests/unit/notion/test_facade.py` (TODO)
- **Focus**: Integrazione moduli, workflow completi

---

## Riepilogo Test Suite

### 📊 **RISULTATI ATTUALI**

- **Total Tests**: 82 test ✅
- **Execution Time**: 0.82s (sub-second performance!)
- **Success Rate**: 100% ✅
- **Coverage**: 4/6 moduli NotionService completamente testati

### 📈 **BREAKDOWN PER MODULO**

| Modulo | Test Count | Runtime | Status |
|--------|------------|---------|---------|
| **NotionDataParser** | 30 test | ~0.21s | ✅ Completato |
| **NotionQueryBuilder** | 17 test | ~0.22s | ✅ Completato |
| **NotionCrudOperations** | 18 test | ~0.24s | ✅ Completato |
| **NotionClient** | 17 test | ~0.66s | ✅ Completato |
| **NotionDiagnostics** | 0 test | - | 📋 TODO |
| **NotionService** (Facade) | 0 test | - | 📋 TODO |

### 🎯 **OBIETTIVI RAGGIUNTI**

✅ **Test Strategy**: Suite completa per verifica funzionamento NotionService  
✅ **Fast Feedback**: Performance sub-second per sviluppo rapido  
✅ **Mock Strategy**: Nessuna chiamata API reale, test isolati e sicuri  
✅ **Edge Case Coverage**: Gestione errori, input malformati, scenari reali  
✅ **Documentation**: Ogni test documentato con contesto business  
✅ **Enterprise Grade**: Architettura modulare testabile e manutenibile

### 🚀 **ESECUZIONE COMPLETA**

```bash
# Esegui tutta la suite Notion (82 test)
pytest tests/unit/notion/ -v

# Solo test specifici con markers
pytest -m "unit and notion" tests/unit/notion/ -v

# Con coverage report
pytest tests/unit/notion/ --cov=app.services.notion --cov-report=term-missing -v
```

---

## Note Tecniche

- **Isolamento**: Ogni test è indipendente, usa fixture dedicate
- **Mocking**: Nessuna chiamata API reale nei unit test
- **Documentazione**: Ogni test ha docstring dettagliata con scopo e verifiche
- **Markers**: `@pytest.mark.unit` e `@pytest.mark.notion` per filtering
- **Performance**: Target < 1s per modulo per feedback rapido durante sviluppo