# 📚 Formazing - App Gestione Formazioni

> Una guida chiara e lineare per gestire formazioni in 3 click, senza stress e senza errori.

## 🔑 Cos'è questa app e perché esiste

### Problema che risolve
*"Devo programmare formazioni per l'associazione, ma ogni volta perdo tempo a creare meeting Teams, inviare email, ricordarmi i codici e gestire i feedback. E se sbaglio a inviare comunicazioni? Panico totale."*

### Soluzione
Un'app semplice come un pulsante che:
- ✅ **Non fa nulla da sola** → solo tu decidi quando agire
- ✅ **Usa Notion come database** (tu inserisci i dati, l'app li trasforma)
- ✅ **Blocca gli errori** (nessun invio accidentale, nessun link rotto)

**Parola chiave: Controllo totale. Tu comandi, l'app obbedisce.**

## 🧩 Architettura Generale

### 1. Notion = Il tuo foglio Excel condiviso

**Cosa contiene:** Solo i dati grezzi delle formazioni (Nome, Area, Data...)  
**Cosa NON contiene:** Formule complesse, automazioni, codici calcolati

#### Struttura del database (campi obbligatori):

| Campo | Esempio | Note |
|-------|---------|------|
| **Nome** | Sicurezza Web | Titolo della formazione |
| **Area** | IT | Dropdown: IT, R&D, HR, Legale, Commerciale, Marketing, All |
| **Data/Ora** | 15/03/2024 14:00 | Data/ora confermata |
| **Periodo** | SPRING | Dropdown: SPRING, AUTUMN, ONCE, EXT, OUT |
| **Stato** | Programmata | Solo 3 opzioni: Programmata, Calendarizzata, Conclusa |
| **Codice** | (vuoto) | L'app lo riempie al momento giusto |
| **Link Teams** | (vuoto) | L'app lo riempie al momento giusto |

#### Tipi di Periodo:
- **SPRING/AUTUMN**: Formazioni periodiche (primavera/autunno)
- **ONCE**: Formazioni una tantum interne
- **EXT**: Formazioni ricevute da esterni (altre JE, aziende, professori)
- **OUT**: Formazioni erogate all'esterno (per altre JE o l'università)

## 🔄 Flusso Operativo Completo

### Fase 1: Crei la formazione in Notion *(tu, in tranquillità)*

1. Apri il database Notion "Formazioni"
2. Clicca "Nuova pagina"
3. Compila solo questi campi:
   - **Nome** → Sicurezza Web
   - **Area** → IT
   - **Data/Ora** → 15/03/2024 14:00
   - **Periodo** → SPRING
   - **Stato** → Programmata (obbligatorio!)
4. Non toccare altri campi (Codice, Link Teams rimangono vuoti)
5. Salva → la formazione è pronta per l'invio

✅ **Perché è sicuro:**
- Nessun invio automatico
- Puoi modificare dati finché lo stato è "Programmata"

### Fase 2: Invii comunicazioni *(1 click nell'app, con anteprima obbligatoria)*

1. **Apri l'app Flask** e accedi con la tua password (protezione Basic Auth)
2. **Vedi SOLO le formazioni** con stato = "Programmata"
3. **Seleziona la formazione** e clicca "Anteprima comunicazioni"
4. **Vedi esattamente** cosa verrà inviato e a chi:

#### Esempio di anteprima:
```
✉️ EMAIL (inviate a: team IT)
Oggetto: [IT] Formazione "Sicurezza Web" il 15/03 - Codice: IT-Sicurezza_Web-2024-SPRING-01

💬 TELEGRAM (gruppo: IT + PRINCIPALE)
Messaggio: 📅 Nuova formazione per IT!
Argomento: Sicurezza Web
Data: 15/03/2024 14:00
```

5. **Se tutto è OK**, clicca "CONFERMA INVIO"

L'app fa **4 cose in sequenza:**
1. Genera il codice → `IT-Sicurezza_Web-2024-SPRING-01`
2. Crea il meeting Teams → link salvato in Notion
3. Invia email alle aree coinvolte, includendo il link Teams
4. Invia messaggi Telegram ai gruppi coinvolti (gruppo area + gruppo principale), incluso il link Teams
5. Aggiorna lo stato → "Calendarizzata"

### Fase 3: Invii i feedback *(1 click nell'app, dopo la formazione)*

1. **Apri l'app Flask** → vai in "Formazioni da chiudere"
2. **Vedi SOLO le formazioni** con stato = "Calendarizzata"
3. **Clicca "INVIA FEEDBACK"**

L'app fa **2 cose:**
1. Cerca il link precompilato in `feedback_links.csv`
2. Invia il link via Telegram ai gruppi coinvolti
3. Aggiorna lo stato → "Conclusa"

## 🚀 Flusso in 3 Passi

1. **In Notion:** Compili i dati base → Stato = "Programmata"
2. **Nell'app:** Clicchi "Invia comunicazioni" → l'app genera codice, crea Teams, invia email/Telegram dopo anteprima
3. **Dopo la formazione:** Clicchi "Invia feedback" → l'app manda il link via Telegram e aggiorna stato a "Conclusa"

**Nessuna complessità nascosta. Nessun rischio. Solo 2 click al mese.**

## 🛡️ Garanzie di Sicurezza

| Scenario | Soluzione nell'app | Risultato |
|----------|-------------------|-----------|
| "Ho paura di inviare per errore" | Password + anteprima obbligatoria + conferma esplicita | Nessun invio accidentale |
| "Non voglio gestire codici complessi" | L'app genera il codice al click | Zero errori umani |
| "Come gestisco i link feedback?" | Script separato genera i link offline | Link sempre pronti |
| "Un collega potrebbe rovinare tutto" | Basic Auth + nessuna azione automatica | Solo tu puoi inviare |
| "Voglio sapere le formazioni del giorno" | Bot Telegram con comandi | Info sempre a portata di mano |

## 🧪 Testing e Validazione

Il sistema include una suite di test completa per garantire affidabilità e sicurezza prima del deploy in produzione.

### 🎯 Scenari di Testing Principali

#### **1️⃣ Test SOLO Componenti Notion (Veloce - 0.9s)**
Testa **tutti i 5 moduli NotionService** senza dipendenze esterne:
```bash
# Usando quick_test.bat
.\quick_test.bat notion

# Oppure direttamente con pytest
python -m pytest tests/unit/notion/ -v
```
**Cosa testa:** Parser dati, Query builder, CRUD operations, Client auth, Service facade  
**Risultato:** 86 test in ~0.9 secondi ✅

#### **2️⃣ Test TUTTE le Componenti (Unit Test Completi - 1.2s)**
Testa **NotionService + TelegramFormatter** - logica pura, zero invii reali:
```bash
# Usando quick_test.bat (RACCOMANDATO)
.\quick_test.bat unit

# Oppure direttamente con pytest  
python -m pytest tests/unit/ -v
```
**Cosa testa:** Tutti i moduli Notion + Formattazione messaggi + Edge cases  
**Risultato:** 106 test in ~1.2 secondi ✅

#### **3️⃣ Test con Invii REALI (Attenzione - 30-60s)**
Testa con **bot Telegram vero** - invia messaggi reali alle chat di test:
```bash
# Test completo interattivo (CON CONFERMA)
.\quick_test.bat interactive

# Test specifici (INVIO DIRETTO)
.\quick_test.bat training    # Solo notifiche formazione
.\quick_test.bat feedback    # Solo richieste feedback  
.\quick_test.bat bot         # Solo comandi bot

# Tutti i test reali insieme (MASSIMA ATTENZIONE)
.\quick_test.bat real
```
**⚠️ ATTENZIONE:** Questi inviano messaggi **reali** alle chat Telegram configurate!

### 📋 Quick Test Script - Guida Completa

#### **🟢 Comandi Sicuri (Zero Invii)**
```bash
.\quick_test.bat check      # Verifica configurazione ambiente (2s)
.\quick_test.bat format     # Preview messaggi senza invio (5s)
.\quick_test.bat notion     # Solo moduli Notion (0.9s)
.\quick_test.bat unit       # Tutti unit test (1.2s) 👈 RACCOMANDATO
```

#### **� Comandi Controllati**
```bash
.\quick_test.bat interactive   # Test completo con conferme esplicite
.\quick_test.bat safe         # Test diagnostici controllati
```

#### **🔴 Comandi con Invio Reale**
```bash
.\quick_test.bat training     # Invia notifica formazione di test
.\quick_test.bat feedback     # Invia richiesta feedback di test
.\quick_test.bat bot          # Attiva bot per 60s (risponde ai comandi)
.\quick_test.bat real         # TUTTI i test con invio reale
```

### 📊 Matrice Test Completa

| Comando | Durata | Invii Reali | Componenti Testate | Uso Raccomandato |
|---------|--------|-------------|-------------------|------------------|
| `unit` | 1.2s | ❌ No | Notion + Telegram | ⭐ **Sviluppo quotidiano** |
| `notion` | 0.9s | ❌ No | Solo Notion | 🔧 Debug Notion specifico |
| `format` | 5s | ❌ No | Formatting + Preview | ✅ Pre-commit validation |
| `interactive` | 30s | ⚠️ Con conferma | Tutto + Invii controllati | 🎯 **Pre-deploy completo** |
| `training` | 10s | ✅ Sì | Solo notifiche formazione | 🔍 Debug invio notifiche |
| `feedback` | 10s | ✅ Sì | Solo richieste feedback | 🔍 Debug invio feedback |
| `bot` | 60s | ✅ Sì | Solo comandi bot | 🤖 Test interattivo bot |
| `real` | 60s | ✅ Sì | **Tutto con invii reali** | ⚠️ **Solo validazione finale** |

### 🏗️ Architettura Test Implementata

- **106 test totali** organizzati in moduli specializzati
- **Fixture modulari** per riutilizzo e manutenibilità  
- **Mock intelligenti** per isolamento senza perdere realismo
- **Test pyramid** ottimizzata: tanti unit test veloci, pochi integration test mirati

## 🏗️ Struttura del Progetto

```
formazioni_app/
├── app/
│   ├── __init__.py           # Inizializza l'app Flask
│   ├── routes.py             # Dashboard principale
│   ├── services/
│   │   ├── notion/             # Servizio Notion (architettura modulare)
│   │   │   ├── __init__.py       # Facade pattern - API unificata
│   │   │   ├── notion_client.py  # Core connection e autenticazione
│   │   │   ├── query_builder.py  # Costruzione query dinamiche
│   │   │   ├── data_parser.py    # Parsing e mapping dati
│   │   │   ├── crud_operations.py # Operazioni CRUD database
│   │   │   └── diagnostics.py    # Monitoring e debugging
│   │   ├── mgraph_service.py   # API Microsoft Graph (Teams, Email)
│   │   ├── telegram_service.py # Messaggi Telegram
│   │   └── training_service.py # Orchestratore principale
│   ├── templates/
│   │   └── index.html          # Dashboard HTML
│   └── static/
│       └── style.css           # Stili CSS
├── tests/
│   ├── conftest.py             # Fixture globali pytest
│   ├── integration/
│   │   └── test_real_telegram.py # Test integrazione reali
│   ├── config/                 # Configurazioni test
│   └── mocks/                  # Mock services
├── config/
│   ├── telegram_groups.json    # Mappa Aree → ID Chat Telegram
│   └── message_templates.yaml  # Template messaggi
├── docs/
│   ├── bot-telegram.md         # Documentazione bot
│   ├── notion-service.md       # Documentazione servizio Notion
│   ├── testing.md             # Documentazione test
│   ├── fixture-testing-guide.md # 📚 Guida completa fixture testing
│   └── fixture-quick-reference.md # 🔧 Reference rapido fixture
├── quick_test.bat              # Script test Windows
├── quick_test.sh               # Script test Linux/Mac
├── .env                        # Chiavi segrete
├── config.py                   # Configurazioni
├── requirements.txt            # Dipendenze Python
└── run.py                      # Avvio applicazione
```

Formazing: la gestione delle formazioni non è mai stata così semplice.