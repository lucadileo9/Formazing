# 🧪 Documentazione Sistema di Test Formazing

> **Guida all'architettura e funzionamento della suite di test - Come capire e modificare il sistema**

## 📋 Indice

1. [Panoramica Sistema](#-panoramica-sistema)
2. [Architettura Test](#-architettura-test)  
3. [Fixture e Meccanismo Dependency Injection](#-fixture-e-meccanismo-dependency-injection)
4. [Test Implementati](#-test-implementati)
5. [Script di Automazione](#-script-di-automazione)
6. [Costrutti e Pattern](#-costrutti-e-pattern)
7. [Connessioni tra Componenti](#-connessioni-tra-componenti)

---

## 🎯 Panoramica Sistema

### Filosofia di Testing

Il sistema di test Formazing segue una **filosofia "Reale ma Controllato"**:

- ✅ **TelegramService REALE** → usa il bot vero, API vere, gruppi veri
- ✅ **Messaggi REALI** → inviati su Telegram, visibili e verificabili
- ❌ **NotionService MOCK** → dati controllati, nessun impatto su database production
- 🏷️ **Marker [TEST]** → tutti i messaggi chiaramente identificabili

### Obiettivi

1. **🔍 Validazione Completa**: Testare l'intero flusso end-to-end
2. **🛡️ Sicurezza**: Ambiente controllato senza rischi per la produzione  
3. **🎯 Precisione**: Verifiche specifiche con assert dettagliati
4. **⚡ Velocità**: Test modulari eseguibili singolarmente
5. **🤖 Automazione**: Script semplificati per workflow ripetibili

---

## 🏗️ Architettura Test

### Struttura File System

```
tests/
├── conftest.py                 # ❤️ CUORE: Fixture globali pytest
├── unit/                       # 🧪 NUOVO: Test unitari velocissimi
│   └── test_telegram_formatter.py  # 📝 Test formattazione messaggi
├── integration/
│   └── test_real_telegram.py   # 🎯 TEST PRINCIPALI: 4 test completi
├── config/
│   ├── test_telegram_groups.json    # 📱 Gruppi Telegram di test
│   └── test_message_templates.yaml  # 📝 Template messaggi test
└── mocks/
    └── mock_notion.py          # 🎭 Mock NotionService con dati controllati
```

### Separazione Responsabilità

| Componente | Responsabilità | Tipo | Velocità |
|------------|----------------|------|----------|
| **conftest.py** | Configurazione globale, fixture condivise | Infrastruttura | - |
| **unit/test_telegram_formatter.py** | Test logica pura formattazione | Unit Logic | ⚡ 0.4s |
| **integration/test_real_telegram.py** | Test business logic, verifiche end-to-end | Integration Logic | 🐌 30-60s |
| **config/** | Dati di configurazione isolati per test | Configuration | - |
| **mocks/** | Simulazione servizi esterni controllati | Mock Layer | - |
| **quick_test.bat/.sh** | Automazione esecuzione, UX semplificata | Automation | - |

---

## ⚡ Unit Test - Logica Pura Velocissima

### Filosofia Unit Test

Gli unit test seguono il principio **"Fast, Isolated, Repeatable"**:

- ⚡ **Velocissimi**: 20 test in 0.4 secondi
- 🔒 **Isolati**: Zero dipendenze esterne (no API, no file, no network)
- 🎯 **Focalizzati**: Testano una singola unità logica per volta
- 🔄 **Ripetibili**: Risultati identici ad ogni esecuzione

### Componenti Testati

#### 📝 **TelegramFormatter** (`test_telegram_formatter.py`)

**Focus**: Logica pura di formattazione messaggi e parsing date

| Categoria Test | Numero Test | Cosa Verifica |
|---------------|-------------|---------------|
| **Training Messages** | 8 test | Template selection, placeholder substitution, error handling |
| **Feedback Messages** | 3 test | Template rendering, link injection, fallback scenarios |
| **Date Parsing** | 6 test | ISO→Italian conversion, custom formats, error handling |
| **Template Logic** | 3 test | Template selection per gruppo, fallback behaviors |

### Vantaggi Unit Test

#### **🚀 Sviluppo Veloce**
- **Instant feedback**: Risultati immediati durante coding
- **Refactoring sicuro**: Modifiche protette da test automatici
- **Debug preciso**: Errori localizzati a singole funzioni

#### **📋 Documentazione Vivente**
- **Esempi d'uso**: Ogni test mostra come usare la funzione
- **Edge cases**: Documentano comportamenti limite
- **Expected behavior**: Specificano cosa deve succedere

---

## 🔧 Fixture e Meccanismo Dependency Injection

### Come Funziona la Gerarchia delle Fixture

Il sistema usa un **pattern Bottom-Up a 4 livelli** dove ogni fixture dipende da quelle del livello inferiore. Questo crea un flusso di configurazione automatico che va dalle configurazioni base fino al service completo.

#### Livello 1: Configurazione Base
- **`load_test_env()`** - Carica il file `.env` e mappa i percorsi di configurazione
- **Scope session** - Eseguita una sola volta per tutta la sessione di test
- **Responsabilità** - Fornire le configurazioni di base (token, paths)

#### Livello 2: Servizi Mock  
- **`mock_notion_service()`** - Crea MockNotionService con dati controllati
- **Scope function** - Nuova istanza per ogni test (isolamento)
- **Responsabilità** - Simulare Notion con dati prevedibili

#### Livello 3: Dati di Test
- **`sample_training_data()`** - Dati formazione per area IT
- **`alternative_training_data()`** - Dati formazione per area HR  
- **`sample_feedback_data()`** - Dati feedback completato
- **Responsabilità** - Fornire dati realistici ma controllati per i test

#### Livello 4: Service Completo (Top Level)
- **`configured_telegram_service()`** - TelegramService completamente configurato
- **Combina** tutti i livelli precedenti in un oggetto pronto all'uso
- **Applica Dependency Injection** - Sostituisce NotionService reale con mock
- **Gestisce fallimenti** - Skip automatico se token mancante

### Meccanismo Dependency Injection

Il cuore del sistema è la **sostituzione trasparente** del NotionService:

1. **TelegramService viene creato normalmente** con configurazioni reali
2. **MockNotionService viene iniettato** tramite `set_notion_service()`  
3. **Il service non sa** di stare usando un mock invece del service reale
4. **I test ottengono comportamento reale** (Telegram) con dati controllati (Notion)

Questo permette di testare l'**intero flusso reale** senza impattare i dati di produzione.

---

## 📊 Test Suite Struttura

### TestRealTelegramIntegration - 4 Test Principali

La classe contiene test specifici per ogni funzionalità del TelegramService, ognuno progettato per verificare un aspetto particolare del sistema:

#### 1. **test_formatter_preview_messages** (SICURO)
- **Obiettivo** - Verifica formattazione messaggi senza invio alcuno
- **Cosa usa** - Formatter interno, template system, tutti i tipi di dati (IT, HR, feedback) 
- **Cosa verifica** - Presenza campi richiesti, lunghezza messaggi, differenze tra gruppi
- **Sicurezza** - **Zero invii**, solo preview e validazione formato

#### 2. **test_send_training_notification_real** (REALE)
- **Obiettivo** - Verifica invio notifiche formazione a tutti i gruppi configurati
- **Cosa usa** - `sample_training_data` fixture con dati IT standard
- **Cosa verifica** - Formato risultati (dict), almeno un messaggio inviato, log dettagliato
- **Particolarità** - Testa l'intero flusso: template → formattazione → invio → risultati

#### 3. **test_send_feedback_notification_real** (REALE)
- **Obiettivo** - Verifica invio feedback con logica anti-spam
- **Cosa usa** - `sample_feedback_data` fixture con stato "Completata"
- **Cosa verifica** - Gestione anti-spam, risultati coerenti anche se vuoti
- **Particolarità** - **Comportamento normale** se nessun gruppo configurato per feedback

#### 4. **test_bot_commands_interactive** (REALE)
- **Obiettivo** - Verifica esecuzione comandi bot in ambiente reale
- **Cosa usa** - Comando `/help` sicuro, chat_id intelligente (main_group o primo disponibile)
- **Cosa verifica** - Infrastruttura comando, gestione errori senza fail
- **Particolarità** - **Non fa fallire il test** se bot offline (testa l'infrastruttura, non il bot)

---

## 🎯 Test Meccanismi Dettagliati

### Meccanismo di Sicurezza "Preview Before Action"

I test usano un **approccio a 2 fasi** per massimizzare sicurezza e debugging:

1. **Preview Phase** - Genera e mostra l'output senza azioni
2. **Action Phase** - Esegue l'azione reale con output completo

Questo permette di:
- **Verificare formato** prima dell'invio
- **Debug visivo** delle formattazioni
- **Controllo manuale** pre-invio per sicurezza
- **Log strutturato** per troubleshooting

### Meccanismo Anti-Spam nei Feedback

Il sistema ha una **logica business specifica** per i feedback:

- **Training notifications** → Vanno a `main_group` + `area_group` (massima visibilità)
- **Feedback requests** → Vanno SOLO ai `area_group` (evita spam nel main)

I test verificano questo comportamento con **negative assertions**:
- Assert che feedback NON vada al main_group
- Educazione inline che spiega perché è corretto

### Meccanismo Fallback Intelligente

Ogni test ha **strategie di fallback** per situazioni comuni:

- **Chat ID mancante** → Usa primo gruppo disponibile
- **Bot offline** → Test non fallisce (testa infrastruttura)
- **Token mancante** → Skip automatico con messaggio chiaro
- **Gruppi non configurati** → Comportamento documentato come normale

### Meccanismo Dependency Injection nei Test

I test dimostrano il **vantaggio principale** del DI pattern:

- **Service reale** per comportamenti autentici (API Telegram)
- **Mock data** per controllo totale (dati Notion)
- **Configurazioni isolate** per evitare conflitti
- **Skip conditionals** per environment diversi

---

## � Guida Scrittura Nuovi Unit Test

### Step-by-Step per Nuovo Componente

#### **1. Identificare l'Unità da Testare**
```python
# ✅ BUONI CANDIDATI per unit test
class DateUtils:                    # Pure functions matematiche
    def parse_notion_date(date_str): pass
    def format_italian_date(dt): pass
    def is_today(date_str): pass

class ConfigValidator:              # Logica validazione
    def validate_groups(config): pass
    def check_required_fields(data): pass

# ❌ CATTIVI CANDIDATI per unit test  
class TelegramService:              # Troppo integration-heavy
class NotionService:                # API calls externe
```

#### **2. Template Completo Nuovo Unit Test**

```python
"""
Test unitari per [ComponentName] - [Brief Description]

[Detailed description of what this module tests]
"""

import pytest
from unittest.mock import patch, Mock
from app.services.my_component import MyComponent

@pytest.mark.unit  
class TestMyComponent:
    """Test suite per MyComponent - Focus su [specific area]"""
    
    # ===== FIXTURE SETUP =====
    @pytest.fixture
    def component(self, dependency_from_conftest):
        """MyComponent configurato per testing"""
        return MyComponent(dependency_from_conftest)
    
    # ===== HAPPY PATH TESTS =====
    def test_main_method_complete_data(self, component, sample_data_from_conftest):
        """
        Test scenario normale con dati completi.
        
        Verifica che:
        - Tutti i campi vengano processati correttamente
        - Il risultato abbia la struttura attesa
        - Non ci siano side effects indesiderati
        """
        result = component.main_method(sample_data_from_conftest)
        
        assert isinstance(result, expected_type)
        assert expected_field in result
        
    # ===== EDGE CASE TESTS =====  
    def test_main_method_missing_data(self, component):
        """
        Test gestione dati incompleti con fallback automatici.
        
        Scenario: Dati con campi mancanti
        Verifica: Fallback corretti, nessun crash
        """
        minimal_data = {'required_field': 'value'}
        
        result = component.main_method(minimal_data)
        
        assert 'fallback_value' in result
        
    # ===== ERROR HANDLING =====
    @patch('app.services.my_component.logger')
    def test_main_method_logs_errors(self, mock_logger, component):
        """
        Test logging automatico errori con mock verification.
        
        Verifica che:
        - Errori vengano loggati correttamente
        - Il sistema non crashi per input invalidi
        - Mock verification funzioni
        """
        component.main_method('invalid_input')
        
        mock_logger.error.assert_called_once()
```

### Best Practices Unit Test

#### **🎯 Naming & Documentation**
- **Nomi descrittivi**: `test_method_scenario_expected_behavior`
- **Docstring dettagliati**: Scenario, verifica, particolarità
- **Assert specifici**: Verifiche precise, non generiche

#### **🔄 Riutilizzo Fixture**  
- **Fixture da conftest.py**: Sempre preferire alle fixture locali
- **Template reali**: Caricare configurazioni di produzione
- **DRY principle**: Zero duplicazione di setup

#### **⚡ Performance**
- **Test isolati**: Ogni test indipendente dagli altri
- **Mock minimali**: Solo dipendenze esterne
- **Execution speed**: Puntare a <1s per test suite

---

## �🚀 Sistema di Automazione

### Architettura quick_test Scripts

Gli script di automazione seguono un **pattern a 3 livelli**:

#### Livello 1: Validazione Prerequisites
- **Verifica .env** - Check token e configurazioni
- **Verifica file config** - test_telegram_groups.json e test_message_templates.yaml
- **Fail-fast approach** - Stop immediato se mancano prerequisiti

#### Livello 2: Mappatura Comando → Test
- **Interface semantica** - Comandi user-friendly invece di sintassi pytest complessa
- **Granularità flessibile** - Da singolo test a suite completa
- **Progressive safety** - Da sicuro (format) a rischioso (real)

#### Livello 3: Esecuzione Ottimizzata
- **Output verboso** - Flag `-s -v` per debugging
- **Traceback corto** - `--tb=short` per errori chiari
- **Targeting preciso** - Esecuzione di singoli metodi pytest


#### Pattern "Command Mapping"

| Comando User | Test Target | Sicurezza |
|-------------|-------------|-----------|
| `format` | `test_formatter_preview_messages` | ✅ Solo preview |
| `training` | `test_send_training_notification_real` | ⚠️ Invio reale |
| `feedback` | `test_send_feedback_notification_real` | ⚠️ Invio reale |
| `bot` | `test_bot_commands_interactive` | ⚠️ Bot attivo 60s |
| `interactive` | Tutti con conferme | ⚠️ Ask before send |
| `real` | Tutti senza conferme | ❌ Auto-send |

---

## 🔗 Connessioni tra Componenti

### Diagramma Archiettura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   quick_test    │───▶│   pytest        │───▶│  conftest.py    │
│   (.bat/.sh)    │    │                 │    │  (fixtures)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  User Interface │    │ TestRealTelegram│    │configured_tele  │
│  Semplificata   │    │  Integration    │    │ gram_service    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Real Tests    │    │ TelegramService │
                       │ (4 test async)  │───▶│    (REALE)      │
                       └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │ MockNotionService│◀───│ Dependency      │
                       │ (dati controllati)│    │ Injection      │
                       └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │ Telegram API    │
                       │ (messaggi REALI)│
                       └─────────────────┘
```

### Flusso Dati

1. **🎮 User Input**: `.\quick_test.bat format`
2. **🔍 Script Validation**: Verifica `.env`, config files
3. **⚡ Pytest Execution**: Esegue test specifico con parametri ottimali
4. **🏭 Fixture Loading**: `conftest.py` configura ambiente
5. **🎯 Service Creation**: `configured_telegram_service` istanziato
6. **🎭 Mock Injection**: `MockNotionService` iniettato nel service reale
7. **📱 Real Telegram**: API calls vere verso Telegram
8. **✅ Assertions**: Verifiche specifiche sui risultati
9. **📊 Output**: Report formattato per l'utente

---
## 📋 Costrutti e Pattern di Design

### 1. Sistema di Marker Pytest
I **marker personalizzati** dividono i test per livello di sicurezza:
- **`@pytest.mark.asyncio`** - Abilita supporto async/await per operazioni Telegram
- **`@pytest.mark.real_telegram`** - Identifica test che inviano messaggi reali

Questo permette esecuzione selettiva:
- Marker `real_telegram` → Solo test con invii reali
- Marker `not real_telegram` → Solo test sicuri (preview)

### 2. Strategia di Scoping delle Fixture
**Session scope** per configurazioni pesanti:
- `load_test_env()` - Carica .env una sola volta per tutta la sessione
- Evita reload multipli di file di configurazione

**Function scope** per dati di test:
- `sample_training_data()` - Nuova istanza per ogni test
- Garantisce isolamento completo tra test

### 3. Dependency Injection Pattern
Il **cuore del sistema** che permette test realistici con dati controllati:

**Service Layer** - TelegramService mantiene interfaccia reale
**Mock Layer** - MockNotionService implementa stessa interfaccia con dati fake
**Injection Point** - Metodo `set_notion_service()` per sostituzione trasparente

Questo pattern elimina la necessità di modificare il codice business per i test.

### 4. Gestione Async/Await
**Async functions** richiedono marker `@pytest.mark.asyncio`
**Await operations** per tutte le chiamate TelegramService (sono async)
**Sync assertions** per verifiche post-chiamata (restano normali)

---
