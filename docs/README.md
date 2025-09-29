# 📚 Formazing - Documentazione

**Sistema di notifiche automatiche per formazioni aziendali tramite Telegram Bot**

## 📋 Indice Generale

### 🏗️ Architettura del Sistema
- [**🤖 Bot Telegram**](bot-telegram.md) - Documentazione completa del sistema bot
- [**🔗 Servizio Notion**](notion-service.md) - Architettura modulare per integrazione Notion API
- [**🧪 Testing & Quality**](testing/) - Sistema di test, fixture e validazione qualità
- **📊 Servizi Core** - Logica di business e orchestrazione *(da documentare)*

---

## 🎯 Quick Start

### Panoramica del Sistema
Formazing è un sistema automatizzato che:
1. **Recupera** informazioni su formazioni aziendali da Notion
2. **Formatta** i dati secondo template configurabili 
3. **Invia** notifiche automatiche via Telegram ai gruppi appropriati
4. **Calendarizza** eventi e invia email tramite Microsoft Graph API
5. **Gestisce** comandi interattivi per consultazioni manuali

### Architettura High-Level
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│   Notion API    │◄───┤  Flask Backend  │───►│ Telegram Bot    │
│   (Formazioni)  │    │   (Orchestr.)   │    │  (Notifiche)    │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Microsoft      │
                    │  Graph API      │
                    │ (Email + Cal.)  │
                    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │                 │
                    │  Configurazione │
                    │ (YAML + JSON)   │
                    │                 │
                    └─────────────────┘
```

### Stack Tecnologico
- **🐍 Python 3.9+** - Linguaggio principale
- **🌐 Flask** - Web framework per API
- **🤖 python-telegram-bot** - SDK Telegram Bot API
- **📄 Notion SDK** - Integrazione database Notion
- **� Microsoft Graph API** - Integrazione email e calendari Outlook
- **�📝 PyYAML** - Gestione template messaggi
- **🔧 python-dotenv** - Gestione variabili ambiente

---

## 📁 Struttura del Progetto

```
Formazing/
├── 📄 README.md                 # Documentazione generale progetto
├── ⚙️ config.py                 # Configurazione Flask
├── 🚀 run.py                    # Entry point applicazione
├── 📦 requirements.txt          # Dipendenze Python
├── 
├── 📂 app/                      # Core dell'applicazione
│   ├── 🔧 __init__.py
│   ├── 🌐 routes.py             # API endpoints Flask
│   │
│   └── 📂 services/             # Logica di business
│       ├── 🔗 mgraph_service.py     # Integrazione Microsoft Graph
│       ├── 📊 notion_service.py     # Connettore Notion API
│       ├── 🎯 training_service.py   # Orchestrazione formazioni
│       ├── 📱 telegram_service.py   # Core Telegram Bot
│       │
│       └── 📂 bot/              # Moduli specializzati bot
│           ├── 🔧 __init__.py
│           ├── ⌨️ telegram_commands.py    # Handler comandi bot
│           └── 🎨 telegram_formatters.py  # Formattazione messaggi
│
├── 📂 config/                   # File di configurazione
│   ├── 📝 message_templates.yaml    # Template messaggi
│   └── 🔧 telegram_groups.json      # Mapping gruppi Telegram
│
├── 📂 docs/                     # Documentazione tecnica
│   ├── 📚 README.md             # Indice documentazione (questo file)
│   ├── 🤖 bot-telegram.md       # Documentazione bot Telegram
│   ├── 🔗 notion-service.md     # Documentazione servizio Notion
│   │
│   └── 📂 testing/              # Documentazione testing e qualità
│       ├── 🧪 testing.md             # Sistema di test e workflow
│       ├── 🔧 fixture-testing-guide.md  # Guida completa fixture
│       ├── 📋 fixture-quick-reference.md # Reference rapido fixture
│       └── ⚡ unit-tests.md          # Documentazione unit testing
│
└── 🎨 Static & Templates        # Assets web (se necessario)
    ├── 📂 static/
    └── 📂 templates/
```

---

## 🔗 Collegamenti Utili

### 📖 Documentazione Specifica
- **[🤖 Sistema Bot Telegram](bot-telegram.md)** - Architettura, comandi, formattazione
- **[🔗 Servizio Notion](notion-service.md)** - Architettura modulare, API, operazioni CRUD
- **[🧪 Testing & Quality Assurance](testing/)** - Sistema di test completo, fixture modulari e workflow
- **Training Service** *(coming soon)* - Logica orchestrazione e business rules
- **Configuration Guide** *(coming soon)* - Setup completo ambiente

#### 🧪 Testing Documentation (docs/testing/)
- **[🧪 Testing System](testing/testing.md)** - Architettura test, script quick_test.bat, workflow
- **[🔧 Fixture Guide](testing/fixture-testing-guide.md)** - Guida completa sistema fixture modulari
- **[📋 Fixture Reference](testing/fixture-quick-reference.md)** - Reference rapido di tutte le fixture
- **[⚡ Unit Tests](testing/unit-tests.md)** - Documentazione unit testing specifici

### 🛠️ Sviluppo
- **API Reference** *(coming soon)* - Endpoints Flask e parametri
- **Database Schema** *(coming soon)* - Struttura dati Notion
- **Deployment Guide** *(coming soon)* - Produzione e staging

### 🔧 Manutenzione
- **Troubleshooting** *(coming soon)* - Problemi comuni e soluzioni
- **Logging Guide** *(coming soon)* - Sistema di logging e debug
- **Performance Tuning** *(coming soon)* - Ottimizzazioni e monitoring

---

## 📞 Contatti

Per supporto tecnico o domande sulla documentazione, contattare il team di sviluppo.

> **Nota**: Questa documentazione è in continuo aggiornamento. Le sezioni marcate con *(coming soon)* o *(da documentare)* verranno completate nelle prossime iterazioni del progetto.