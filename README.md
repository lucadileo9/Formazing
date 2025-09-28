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

## ⚙️ Configurazione Iniziale

### In Notion
- Crea il database "Formazioni" con i campi obbligatori
- Non aggiungere formule → lascia Codice e Link Teams vuoti

### Nell'app Flask
- Configura Basic Auth con una password sicura
- Crea il file `templates/config.yaml` con i template base

### Telegram Bot
Il bot deve essere aggiunto ai seguenti gruppi:
- Gruppo principale (tutta l'associazione)
- Gruppi per area: IT, R&D, HR, Legale, Commerciale, Marketing

#### Comandi disponibili:
- `/oggi`: Mostra le formazioni di oggi
- `/domani`: Mostra le formazioni di domani
- `/settimana`: Mostra tutte le formazioni della settimana

### Script esterno per feedback
- Legge TUTTE le formazioni con stato = "Calendarizzata" da Notion
- Per ogni formazione, genera il link precompilato con Selenium
- Quando lanciarlo: dopo aver aggiunto nuove formazioni o modificato il template Microsoft Forms

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

### Script di Test Rapido

```bash
# 🟢 Test unitari (velocissimi, zero dipendenze)
.\quick_test.bat unit

# 🟢 Test sicuro (solo preview, nessun invio)
.\quick_test.bat format

# 🟡 Test completo interattivo (raccomandato)
.\quick_test.bat interactive

# 🔴 Test specifici (invio reale)
.\quick_test.bat training   # Solo test notifiche formazione
.\quick_test.bat feedback   # Solo test feedback
.\quick_test.bat bot        # Solo test comandi bot
```

### Comandi Disponibili

| Comando | Sicurezza | Tempo | Descrizione |
|---------|-----------|-------|-------------|
| `unit` | 🟢 Sicurissimo | ~0.4s | Test logica pura (formattazione, parsing) |
| `check` | 🟢 Sicuro | ~2s | Verifica configurazione ambiente |
| `format` | 🟢 Sicuro | ~5s | Preview messaggi (NO invio) |
| `safe` | 🟢 Sicuro | ~5s | Test diagnostici (NO invio) |
| `training` | 🔴 Reale | ~10s | Test invio notifiche formazione |
| `feedback` | 🔴 Reale | ~10s | Test invio richieste feedback |
| `bot` | 🔴 Reale | ~60s | Test comandi bot (60s attivo) |
| `interactive` | 🟡 Chiede conferma | ~30s | Test completo con scelte |
| `real` | 🔴 Attenzione | ~60s | Tutti i test con invio reale |

### Workflow di Testing Raccomandato

#### 🚀 **Durante Sviluppo** (Developer Workflow)
1. **Setup iniziale**: `.\quick_test.bat check` - Verifica ambiente
2. **Sviluppo attivo**: `.\quick_test.bat unit` - Test istantanei (0.4s)
3. **Test funzionalità**: `.\quick_test.bat format` - Preview sicure
4. **Pre-commit**: `.\quick_test.bat interactive` - Validazione completa

#### 🎯 **Prima del Deploy** (Production Workflow)  
1. **Test sicuri**: `.\quick_test.bat unit` + `.\quick_test.bat format`
2. **Test controllati**: `.\quick_test.bat interactive` - Con conferme
3. **Validazione finale**: `.\quick_test.bat real` - Solo se strettamente necessario

### Tipologie di Test

#### 🧪 **Unit Test** (Nuovo!)
- **⚡ Velocissimi**: 20 test in 0.4 secondi
- **🔒 Zero dipendenze**: Testano logica pura (parsing date, formattazione)
- **📋 Copertura completa**: TelegramFormatter con tutti gli edge cases
- **🎯 Fixture condivise**: Riutilizzano dati da conftest.py
- **🔄 Pattern DRY**: Template reali caricati da YAML

#### 🔗 **Integration Test**
- **🎯 Precisi**: Assert specifici con verifiche dettagliate
- **🛡️ Sicuri**: Test formatazione mai inviano messaggi reali
- **🔍 Completi**: Coprono formattazione, invio, comandi bot
- **📱 Reali**: Usano bot Telegram vero con dati mock controllati
- **🏷️ Marcati**: Tutti i messaggi di test hanno `[TEST]`

#### 🏗️ **Architettura Test**
- **conftest.py**: Fixture centrali condivise (DRY principle)
- **tests/unit/**: Test logica pura, velocissimi
- **tests/integration/**: Test end-to-end con servizi reali
- **Mock intelligenti**: NotionService mock + TelegramService reale

> 📖 **Documentazione completa**: Vedi [`docs/testing.md`](docs/testing.md) per dettagli tecnici e architettura dei test.

## 🏗️ Struttura del Progetto

```
formazioni_app/
├── app/
│   ├── __init__.py           # Inizializza l'app Flask
│   ├── routes.py             # Dashboard principale
│   ├── services/
│   │   ├── notion_service.py   # API Notion
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
│   └── testing.md             # Documentazione test
├── quick_test.bat              # Script test Windows
├── quick_test.sh               # Script test Linux/Mac
├── .env                        # Chiavi segrete
├── config.py                   # Configurazioni
├── requirements.txt            # Dipendenze Python
└── run.py                      # Avvio applicazione
```

Formazing: la gestione delle formazioni non è mai stata così semplice.