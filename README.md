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

Il progetto include un sistema di test completo per garantire affidabilità e sicurezza in produzione.

**Per informazioni complete sui test**: [docs/testing/README.md](docs/testing/README.md)

## 📚 Documentazione

Per informazioni dettagliate su architettura, API e configurazione:

**Documentazione completa**: [docs/README.md](docs/README.md)

## 🏗️ Struttura del Progetto

```
Formazing/
├── app/
│   ├── __init__.py           # Inizializza l'app Flask
│   ├── routes.py             # Dashboard principale e API endpoints
│   ├── services/
│   │   ├── notion/             # Servizio Notion (architettura modulare)
│   │   │   ├── __init__.py       # Facade pattern - API unificata
│   │   │   ├── notion_client.py  # Core connection e autenticazione
│   │   │   ├── query_builder.py  # Costruzione query dinamiche
│   │   │   ├── data_parser.py    # Parsing e mapping dati
│   │   │   ├── crud_operations.py # Operazioni CRUD database
│   │   │   └── diagnostics.py    # Monitoring e debugging
│   │   ├── bot/                # Sistema bot Telegram
│   │   │   ├── telegram_commands.py  # Handler comandi bot
│   │   │   └── telegram_formatters.py # Formattazione messaggi
│   │   ├── mgraph_service.py   # API Microsoft Graph (Teams, Email)
│   │   ├── telegram_service.py # Orchestratore Telegram
│   │   └── training_service.py # Orchestratore principale
│   ├── templates/              # Template web Jinja2
│   │   ├── layout/               # Layout base e strutture
│   │   │   ├── base.html           # Template base principale
│   │   │   └── auth_required.html  # Layout con autenticazione
│   │   ├── pages/                # Pagine complete
│   │   ├── organisms/            # Componenti complessi riutilizzabili
│   │   ├── molecules/            # Componenti medi (form, card, ecc.)
│   │   ├── atoms/                # Componenti base (button, icon, ecc.)
│   │   │   ├── badge.html          # Badge di stato
│   │   │   ├── button.html         # Bottoni
│   │   │   ├── card.html           # Card containers
│   │   │   ├── icon.html           # Icone
│   │   │   └── loading.html        # Indicatori caricamento
│   │   ├── legacy/               # Template legacy (deprecati)
│   │   └── error.html            # Pagina errori
│   └── static/                 # Assets statici
│       └── style.css             # Fogli di stile CSS
├── tests/
│   ├── conftest.py             # Configurazione pytest
│   ├── fixtures/               # Fixture modulari per test
│   ├── unit/                   # Unit test componenti
│   ├── integration/            # Test integrazione reali
│   ├── e2e/                    # Test end-to-end workflow
│   ├── config/                 # Configurazioni test
│   └── mocks/                  # Mock services
├── config/
│   ├── telegram_groups.json    # Mappa Aree → ID Chat Telegram
│   └── message_templates.yaml  # Template messaggi
├── docs/
│   ├── README.md               # Documentazione generale
│   ├── bot-telegram.md         # Documentazione bot
│   ├── notion-service.md       # Documentazione servizio Notion
│   ├── templates/              # Documentazione sistema template
│   │   └── README.md             # Guida atomic design e componenti
│   └── testing/                # Documentazione testing
│       ├── README.md             # Guida testing generale
│       ├── fixture-testing-guide.md # Guida completa fixture
│       └── fixture-quick-reference.md # Reference rapido fixture
├── quick_test.bat              # Script test Windows
├── quick_test.sh               # Script test Linux/Mac
├── .env                        # Variabili ambiente
├── config.py                   # Configurazioni Flask
├── requirements.txt            # Dipendenze Python
└── run.py                      # Entry point applicazione
```

---

**Formazing: la gestione delle formazioni non è mai stata così semplice.**