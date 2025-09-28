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
├── integration/
│   └── test_real_telegram.py   # 🎯 TEST PRINCIPALI: 4 test completi
├── config/
│   ├── test_telegram_groups.json    # 📱 Gruppi Telegram di test
│   └── test_message_templates.yaml  # 📝 Template messaggi test
└── mocks/
    └── mock_notion.py          # 🎭 Mock NotionService con dati controllati
```

### Separazione Responsabilità

| Componente | Responsabilità | Tipo |
|------------|----------------|------|
| **conftest.py** | Configurazione globale, fixture condivise | Infrastruttura |
| **test_real_telegram.py** | Test business logic, verifiche end-to-end | Test Logic |
| **config/** | Dati di configurazione isolati per test | Configuration |
| **mocks/** | Simulazione servizi esterni controllati | Mock Layer |
| **quick_test.bat/.sh** | Automazione esecuzione, UX semplificata | Automation |

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

## 🚀 Sistema di Automazione

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
