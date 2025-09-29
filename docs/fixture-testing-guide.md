# Guida Completa alle Fixture di Test - Formazing Bot

## 📚 Indice

1. [Che cos'è una Fixture](#che-cosè-una-fixture)
2. [Struttura Modulare Implementata](#struttura-modulare-implementata)
3. [Divisione per File](#divisione-per-file)
4. [Documentazione Dettagliata delle Fixture](#documentazione-dettagliata-delle-fixture)
5. [Come Utilizzare le Fixture](#come-utilizzare-le-fixture)
6. [Best Practices](#best-practices)

---

## 🔧 Che cos'è una Fixture

### Definizione
Una **fixture** in pytest è una funzione che fornisce dati o configurazioni standardizzate per i test. È un meccanismo per preparare e fornire risorse necessarie per l'esecuzione dei test in modo consistente e riutilizzabile.

### Caratteristiche Principali

#### 1. **Riutilizzabilità**
```python
@pytest.fixture
def sample_user():
    return {"name": "Mario", "email": "mario@example.com"}

# Può essere usata in più test
def test_user_name(sample_user):
    assert sample_user["name"] == "Mario"

def test_user_email(sample_user):
    assert "@" in sample_user["email"]
```

#### 2. **Scopo (Scope)**
- `function`: Ricreata per ogni test (default)
- `class`: Una per classe di test
- `module`: Una per modulo
- `session`: Una per sessione di test

#### 3. **Dependency Injection**
pytest automaticamente inietta le fixture nei parametri dei test:
```python
def test_example(sample_user, mock_database):
    # pytest fornisce automaticamente entrambe le fixture
    pass
```

### Vantaggi delle Fixture

1. **🧹 DRY (Don't Repeat Yourself)**: Evita duplicazione di codice di setup
2. **🔒 Isolamento**: Ogni test ha dati freschi e isolati
3. **🧪 Consistenza**: Stessi dati di test in tutto il progetto
4. **🔧 Manutenibilità**: Cambi centrali si propagano a tutti i test
5. **📖 Leggibilità**: Test più puliti e focalizzati sulla logica

---

## 🏗️ Struttura Modulare Implementata

### Architettura "Split per Domain/Modulo"

Il nostro progetto implementa una **modularizzazione per dominio** delle fixture:

```
tests/
├── conftest.py                     # Core fixtures (70 righe)
├── conftest_backup.py             # Backup versione originale (900 righe)
└── fixtures/                      # 📁 Fixture organizzate per dominio
    ├── __init__.py                # 🔗 Import centralizzato
    ├── telegram_fixtures.py       # 🤖 Telegram & Training Data
    ├── notion_fixtures.py         # 📄 Base Notion Pages & Responses  
    ├── query_builder_fixtures.py  # 🔍 Query Building & Validation
    ├── crud_fixtures.py          # 💾 CRUD Operations & Mock Clients
    ├── client_fixtures.py        # 🔑 Client Authentication & Environment
    └── facade_fixtures.py        # 🏢 Service Integration & Orchestration
```

### Principi di Design

#### 1. **Separazione delle Responsabilità**
Ogni file gestisce **un dominio specifico** del testing:
- `telegram_fixtures.py` → Solo roba Telegram
- `notion_fixtures.py` → Solo roba Notion base
- etc.

#### 2. **Import Automatico**
```python
# In tests/fixtures/__init__.py
from .telegram_fixtures import *
from .notion_fixtures import *
# ... tutti gli altri

# Nei test rimane semplice:
def test_something(mock_telegram_bot, sample_notion_page):
    pass  # fixture disponibili automaticamente
```

#### 3. **Compatibilità Backwards**
Tutti i test esistenti continuano a funzionare **senza modifiche**.

---

## 📂 Divisione per File

### `conftest.py` - Core Fixtures (70 righe)
**Ruolo**: Fixture essenziali e globali per l'intera suite di test.

**Contenuto**:
- `event_loop`: Event loop asyncio per test asincroni
- `load_test_env`: Variabili d'ambiente
- `mock_training_service`: Mock service di training 
- `test_config`: Configurazioni globali test

**Perché qui**: Fixture utilizzate **trasversalmente** da più domini.

---

### `fixtures/telegram_fixtures.py` - Telegram & Training
**Ruolo**: Mock e dati per testing del sistema Telegram.

**Fixture** (6 totali):
- `mock_telegram_bot`: Bot Telegram mockato
- `configured_telegram_service`: Service configurato
- `sample_training_data`: Dati di training standard
- `alternative_training_data`: Dati alternativi per edge cases
- `sample_feedback_data`: Dati feedback utenti

**Perché separato**: Il dominio Telegram ha logiche specifiche (async, API calls, formatting) che meritano isolamento.

---

### `fixtures/notion_fixtures.py` - Base Notion Data
**Ruolo**: Strutture dati base di Notion (pages, responses).

**Fixture** (8 totali):
- `sample_notion_page`: Page Notion completa
- `sample_notion_page_minimal`: Page con dati minimi
- `sample_notion_page_incomplete`: Page con dati mancanti
- `notion_query_response`: Response API Notion standard
- `notion_page_malformed_date`: Page con date malformate
- `notion_page_rich_text_complex`: Rich text complessi
- `mock_notion_data_parser`: Parser mockato
- `mock_notion_service`: Service mockato

**Perché separato**: Le strutture dati Notion sono complesse e utilizzate da **tutti** i moduli Notion.

---

### `fixtures/query_builder_fixtures.py` - Query Building
**Ruolo**: Query Notion e validazione per test QueryBuilder.

**Fixture** (6 totali):
- `sample_database_id`: ID database standard
- `expected_status_query`: Query filtro status
- `expected_date_range_query`: Query range date
- `expected_area_query`: Query filtro area
- `expected_combined_query`: Query multi-filtro
- `invalid_query_samples`: Query invalide per error testing

**Perché separato**: Le query Notion hanno sintassi complessa e logiche di validazione specifiche.

---

### `fixtures/crud_fixtures.py` - CRUD Operations
**Ruolo**: Mock e responses per operazioni CRUD su Notion.

**Fixture** (8 totali):
- `mock_notion_client`: Client Notion mockato
- `sample_notion_id`: ID Notion standard
- `sample_update_response`: Response update operation
- `sample_retrieve_response`: Response retrieve operation
- `sample_batch_formazioni_ids`: Lista ID per batch ops
- `sample_multiple_fields_update`: Dati update multipli
- `mock_data_parser`: Parser per retrieve ops
- `mock_api_error`: Mock errori API

**Perché separato**: Le operazioni CRUD hanno cicli di vita e error handling specifici.

---

### `fixtures/client_fixtures.py` - Client & Environment
**Ruolo**: Autenticazione, client Notion e variabili d'ambiente.

**Fixture** (7 totali):
- `valid_notion_token`: Token valido per test
- `valid_database_id`: Database ID valido
- `mock_notion_client_class`: Mock classe Client
- `mock_env_variables`: Environment completo
- `mock_env_missing_token`: Environment senza token
- `mock_env_missing_database_id`: Environment senza DB ID
- `mock_env_empty`: Environment vuoto

**Perché separato**: La gestione dell'autenticazione e environment ha requisiti di sicurezza e testing specifici.

---

### `fixtures/facade_fixtures.py` - Service Integration
**Ruolo**: Mock per test d'integrazione e orchestrazione moduli.

**Fixture** (4 totali):
- `mock_notion_service_modules`: Mock completo tutti i moduli
- `sample_facade_formazioni_response`: Response integrate
- `mock_notion_api_response`: Response API simulate
- `facade_error_scenarios`: Scenari errore integrazione

**Perché separato**: I test d'integrazione richiedono orchestrazione complessa di più moduli.

---

## 📖 Documentazione Dettagliata delle Fixture

### 🤖 Telegram Fixtures (`telegram_fixtures.py`)

#### `mock_telegram_bot`
```python
@pytest.fixture
def mock_telegram_bot():
    """Mock completo del bot Telegram per test."""
```
**Scopo**: Simula il bot Telegram per test senza chiamate API reali.
**Utilizzo**: Test invio messaggi, gestione comandi, error handling.
**Mock Configurati**: 
- `send_message()` → return `True`
- `get_me()` → return bot info
- Rate limiting simulato

#### `configured_telegram_service`
```python
@pytest.fixture
def configured_telegram_service(mock_telegram_bot, load_test_env):
    """Service Telegram configurato con mock bot."""
```
**Scopo**: Service Telegram pronto all'uso con configurazioni test.
**Utilizzo**: Test end-to-end del service senza dipendenze esterne.
**Dependencies**: `mock_telegram_bot`, `load_test_env`

#### `sample_training_data`
```python
@pytest.fixture
def sample_training_data():
    """Dati di training standard per test bot."""
```
**Scopo**: Dataset consistente per test training del bot.
**Struttura**:
```python
{
    "nome": "Python Avanzato",
    "area": "IT", 
    "data_inizio": "2024-04-15T14:00:00",
    "docente": "Mario Rossi",
    "link_teams": "https://teams.microsoft.com/test"
}
```

#### `alternative_training_data`
```python
@pytest.fixture  
def alternative_training_data():
    """Dati alternativi per test edge cases."""
```
**Scopo**: Dati diversi per test variabilità e robustezza.
**Differenze**: Nomi lunghi, caratteri speciali, date edge case.

#### `sample_feedback_data`
```python
@pytest.fixture
def sample_feedback_data():
    """Dati feedback utenti per test."""
```
**Scopo**: Simula feedback reali per test parsing e processing.
**Campi**: rating, commento, timestamp, user_id.

---

### 📄 Notion Base Fixtures (`notion_fixtures.py`)

#### `sample_notion_page`
```python
@pytest.fixture
def sample_notion_page():
    """Page Notion completa con tutti i campi."""
```
**Scopo**: Struttura dati Notion standard per test parsing.
**Campi Inclusi**: Nome, Area, Date, Stato, Codice, Link Teams, Periodo.
**Utilizzo**: Test parsing completo, validazione dati.

#### `sample_notion_page_minimal`
```python
@pytest.fixture
def sample_notion_page_minimal():
    """Page Notion con solo campi essenziali."""
```
**Scopo**: Test robustezza con dati minimi.
**Campi**: Solo Nome e ID.
**Utilizzo**: Test edge case, parsing parziale.

#### `sample_notion_page_incomplete`
```python
@pytest.fixture  
def sample_notion_page_incomplete():
    """Page Notion con campi mancanti."""
```
**Scopo**: Test gestione dati incompleti.
**Missing**: Date, Link Teams, Codice.
**Utilizzo**: Test error handling, default values.

#### `notion_query_response`
```python
@pytest.fixture
def notion_query_response():
    """Response standard API query Notion."""
```
**Scopo**: Simula response reali da Notion API.
**Struttura**: Array di pages, has_more, next_cursor.
**Utilizzo**: Test query processing, pagination.

#### `notion_page_malformed_date`
```python
@pytest.fixture
def notion_page_malformed_date():
    """Page con date malformate per test robustezza."""
```
**Scopo**: Test parsing date invalide.
**Date Issues**: Formati non standard, timezone mancanti.
**Utilizzo**: Test error recovery.

#### `notion_page_rich_text_complex`
```python
@pytest.fixture
def notion_page_rich_text_complex():
    """Page con rich text complessi."""
```
**Scopo**: Test parsing rich text Notion.
**Contenuto**: Multi-part text, formatting, links.
**Utilizzo**: Test estrazione testo pulito.

#### `mock_notion_data_parser`
```python
@pytest.fixture
def mock_notion_data_parser():
    """Parser Notion mockato."""
```
**Scopo**: Mock parser per test isolati.
**Methods**: `parse_single_formazione()`, `parse_formazioni_list()`.
**Returns**: Dati parsed consistenti.

#### `mock_notion_service`
```python
@pytest.fixture
def mock_notion_service():
    """Service Notion completo mockato."""
```
**Scopo**: Mock service per test integration.
**Methods**: Tutti i metodi pubblici del service.
**Behavior**: Response predefinite, error simulation.

---

### 🔍 Query Builder Fixtures (`query_builder_fixtures.py`)

#### `sample_database_id`
```python
@pytest.fixture
def sample_database_id():
    """Database ID standard per test query."""
```
**Scopo**: ID consistente per tutte le query test.
**Formato**: UUID valido Notion.
**Utilizzo**: Test query building, validazione.

#### `expected_status_query`
```python
@pytest.fixture
def expected_status_query():
    """Query attesa per filtro status."""
```
**Scopo**: Query di riferimento per test status filter.
**Filtro**: `status.equals = "Programmata"`
**Include**: Sorts, page_size.

#### `expected_date_range_query`
```python
@pytest.fixture
def expected_date_range_query():
    """Query attesa per range date."""
```
**Scopo**: Query di riferimento per test date range.
**Filtri**: `date.on_or_after` + `date.on_or_before`
**Logica**: AND combination.

#### `expected_area_query`
```python
@pytest.fixture  
def expected_area_query():
    """Query attesa per filtro area."""
```
**Scopo**: Query di riferimento per test area filter.
**Filtro**: `multi_select.contains = "IT"`
**Utilizzo**: Test area filtering logic.

#### `expected_combined_query`
```python
@pytest.fixture
def expected_combined_query():
    """Query attesa per filtri combinati."""
```
**Scopo**: Query complessa multi-filtro.
**Combinazione**: Status + Area in AND.
**Utilizzo**: Test query complex building.

#### `invalid_query_samples`
```python
@pytest.fixture
def invalid_query_samples():
    """Esempi di query invalide per test validazione."""
```
**Scopo**: Dataset query malformate.
**Casi**: Missing database_id, empty query, None query.
**Utilizzo**: Test input validation.

---

### 💾 CRUD Fixtures (`crud_fixtures.py`)

#### `mock_notion_client`
```python
@pytest.fixture
def mock_notion_client():
    """Mock client Notion per test CRUD operations."""
```
**Scopo**: Client mockato per operazioni CRUD.
**Mock API**: `pages.update()`, `pages.retrieve()`, `databases.query()`.
**Responses**: Success/error configurabili.

#### `sample_notion_id`
```python
@pytest.fixture
def sample_notion_id():
    """ID Notion standard per test."""
```
**Scopo**: ID consistente per test CRUD.
**Formato**: UUID valido format.
**Utilizzo**: Update, retrieve, delete operations.

#### `sample_update_response`
```python
@pytest.fixture
def sample_update_response():
    """Response simulata per update operations."""
```
**Scopo**: Response API update standard.
**Campi**: object, id, properties updated.
**Utilizzo**: Test update success handling.

#### `sample_retrieve_response`
```python
@pytest.fixture
def sample_retrieve_response():
    """Response simulata per retrieve operation."""
```
**Scopo**: Response API retrieve completa.
**Contenuto**: Page completa con tutti i fields.
**Utilizzo**: Test retrieve + parsing pipeline.

#### `sample_batch_formazioni_ids`
```python
@pytest.fixture
def sample_batch_formazioni_ids():
    """Lista di ID per test batch operations."""
```
**Scopo**: Set ID per test operazioni batch.
**Contenuto**: Array di 3 ID test.
**Utilizzo**: Test batch update, bulk operations.

#### `sample_multiple_fields_update`
```python
@pytest.fixture
def sample_multiple_fields_update():
    """Dati per test update multipli campi."""
```
**Scopo**: Payload update multi-field.
**Campi**: status, codice, link_teams.
**Utilizzo**: Test complex update operations.

#### `mock_data_parser` 
```python
@pytest.fixture
def mock_data_parser():
    """Mock parser per test retrieve operations."""
```
**Scopo**: Parser mockato per retrieve tests.
**Method**: `parse_single_formazione()`.
**Return**: Formazione parsed standard.

#### `mock_api_error`
```python
@pytest.fixture
def mock_api_error():
    """Mock APIResponseError per test gestione errori."""
```
**Scopo**: Errore API per test error handling.
**Type**: `APIResponseError` con status_code 404.
**Utilizzo**: Test error recovery, retry logic.

---

### 🔑 Client Fixtures (`client_fixtures.py`)

#### `valid_notion_token`
```python
@pytest.fixture
def valid_notion_token():
    """Token Notion valido per test."""
```
**Scopo**: Token autenticazione consistente.
**Formato**: `secret_test-token-{uuid}`.
**Utilizzo**: Test autenticazione, client init.

#### `valid_database_id`
```python
@pytest.fixture
def valid_database_id():
    """Database ID valido per test."""
```
**Scopo**: Database ID consistente.
**Formato**: UUID standard.
**Utilizzo**: Test database connection, queries.

#### `mock_notion_client_class`
```python
@pytest.fixture
def mock_notion_client_class():
    """Mock della classe Client di notion-client."""
```
**Scopo**: Mock classe Client per test isolation.
**Patch**: `app.services.notion.notion_client.Client`.
**Utilizzo**: Test client creation, API calls.

#### `mock_env_variables`
```python
@pytest.fixture
def mock_env_variables(valid_notion_token, valid_database_id):
    """Mock delle variabili d'ambiente per test."""
```
**Scopo**: Environment completo per test.
**Variables**: `NOTION_TOKEN`, `NOTION_DATABASE_ID`.
**Utilizzo**: Test environment-based config.

#### `mock_env_missing_token`
```python
@pytest.fixture
def mock_env_missing_token(valid_database_id):
    """Mock con token mancante per test errori."""
```
**Scopo**: Test error handling token mancante.
**Missing**: `NOTION_TOKEN`.
**Utilizzo**: Test initialization errors.

#### `mock_env_missing_database_id`
```python
@pytest.fixture
def mock_env_missing_database_id(valid_notion_token):
    """Mock con database ID mancante per test errori."""
```
**Scopo**: Test error handling DB ID mancante.
**Missing**: `NOTION_DATABASE_ID`.
**Utilizzo**: Test config validation.

#### `mock_env_empty`
```python
@pytest.fixture
def mock_env_empty():
    """Mock con tutte le variabili d'ambiente vuote."""
```
**Scopo**: Test total config failure.
**Environment**: Completamente vuoto.
**Utilizzo**: Test graceful degradation.

---

### 🏢 Facade Fixtures (`facade_fixtures.py`)

#### `mock_notion_service_modules`
```python
@pytest.fixture
def mock_notion_service_modules():
    """Mock completo moduli NotionService per test facade."""
```
**Scopo**: Mock orchestrazione completa moduli.
**Mock Modules**: Client, QueryBuilder, DataParser, CrudOperations, Diagnostics.
**Configuration**: Mock instances con behavior predefinito.
**Utilizzo**: Test integrazione facade, module communication.

#### `sample_facade_formazioni_response`
```python
@pytest.fixture
def sample_facade_formazioni_response():
    """Response simulata per metodi get_formazioni_* della facade."""
```
**Scopo**: Response integrate end-to-end.
**Contenuto**: Array formazioni complete.
**Utilizzo**: Test facade API contract.

#### `mock_notion_api_response`
```python
@pytest.fixture
def mock_notion_api_response():
    """Mock response API Notion per test facade integration."""
```
**Scopo**: Response API per test integration.
**Formato**: Response list con results.
**Utilizzo**: Test API → facade → output pipeline.

#### `facade_error_scenarios`
```python
@pytest.fixture
def facade_error_scenarios():
    """Scenari di errore per test facade error handling."""
```
**Scopo**: Set errori per test robustezza.
**Errors**: Initialization, API, parsing, validation errors.
**Utilizzo**: Test error propagation, recovery strategies.

---

## 🚀 Come Utilizzare le Fixture

### Import Automatico
Grazie alla struttura modulare, tutte le fixture sono **automaticamente disponibili**:

```python
# Non serve import esplicito!
def test_telegram_integration(mock_telegram_bot, sample_training_data):
    # Fixture disponibili direttamente
    pass

def test_notion_parsing(sample_notion_page, mock_notion_data_parser):
    # Anche fixture da moduli diversi
    pass
```

### Combinazione di Fixture
Le fixture possono essere **combinate liberamente**:

```python
def test_complete_workflow(
    configured_telegram_service,      # Da telegram_fixtures.py
    sample_notion_page,              # Da notion_fixtures.py  
    expected_status_query,           # Da query_builder_fixtures.py
    mock_notion_client,              # Da crud_fixtures.py
    valid_notion_token,              # Da client_fixtures.py
    mock_notion_service_modules      # Da facade_fixtures.py
):
    # Test cross-module integration
    pass
```

### Override di Fixture
È possibile **sovrascrivere** fixture per test specifici:

```python
@pytest.fixture
def sample_training_data():
    """Override per test specifico."""
    return {"nome": "Test Speciale", "area": "CUSTOM"}

def test_custom_case(sample_training_data):
    # Usa la fixture overridata
    assert sample_training_data["area"] == "CUSTOM"
```

---

## ✅ Best Practices

### 1. **Naming Convention**
- `sample_*`: Dati esempio per test
- `mock_*`: Mock objects e services  
- `expected_*`: Risultati attesi per assertions
- `valid_*`: Dati validi per test positivi
- `invalid_*`: Dati invalidi per test negativi

### 2. **Documentazione Fixture**
Ogni fixture deve avere **docstring chiara**:
```python
@pytest.fixture
def sample_training_data():
    """
    Dati di training standard per test bot.
    
    Returns:
        dict: Formazione completa con tutti i campi richiesti
        
    Usage:
        Test parsing, formatting, invio messaggi Telegram
    """
    return {...}
```

### 3. **Gestione Scope**
Usa lo **scope appropriato**:
- `function`: Dati che devono essere fresh per ogni test
- `module`: Setup costosi condivisi nel modulo  
- `session`: Configurazioni globali (database connections, etc.)

### 4. **Dependency Management**
Le fixture possono **dipendere tra loro**:
```python
@pytest.fixture
def configured_service(mock_client, valid_token):
    """Service che dipende da altre fixture."""
    return Service(client=mock_client, token=valid_token)
```

### 5. **Parametrizzazione**
Per testare **multiple variations**:
```python
@pytest.fixture(params=["IT", "HR", "MARKETING"])
def area_variants(request):
    """Test con diverse aree."""
    return request.param

def test_area_filtering(area_variants, expected_area_query):
    # Test eseguito 3 volte con aree diverse
    pass
```

### 6. **Cleanup**
Per fixture che richiedono **cleanup**:
```python
@pytest.fixture
def temp_database():
    """Database temporaneo."""
    db = create_temp_database()
    yield db  # Test uses db here
    db.cleanup()  # Cleanup after test
```

---

## 📊 Statistiche Finali

- **Fixture Totali**: 39 fixture
- **File Moduli**: 6 file specializzati
- **Riduzione conftest.py**: Da 900 → 70 righe (-92%)
- **Test Coverage**: 106 test passanti
- **Performance**: Mantenute (1.18s totali)
- **Backwards Compatibility**: 100% 

**La struttura modulare garantisce scalabilità, manutenibilità e qualità del testing per il progetto Formazing Bot.** 🎉