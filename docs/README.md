# 📚 Formazing - Documentazione

**Sistema di notifiche automatiche per├── 📂 services/             # Logica di business
│       ├── 🔗 mgraph_service.py     # Integrazione Microsoft Graph
│       ├── 📊 notion/               # Servizio Notion (architettura modulare)
│       │   ├── 🔧 __init__.py            # Facade pattern - API unificata
│       │   ├── 🔌 notion_client.py       # Core connection e autenticazione
│       │   ├── 🔍 query_builder.py       # Costruzione query dinamiche
│       │   ├── 📄 data_parser.py         # Parsing e mapping dati
│       │   ├── 💾 crud_operations.py     # Operazioni CRUD database
│       │   └── 🔬 diagnostics.py         # Monitoring e debugging
│       ├── 🎯 training_service.py   # Orchestrazione formazioni
│       ├── 📱 telegram_service.py   # Core Telegram Botazioni aziendali tramite Telegram Bot**

## 📋 Indice Generale

### 🏗️ Architettura del Sistema
- [**🤖 Bot Telegram**](bot-telegram.md) - Documentazione completa del sistema bot
- [**🔗 Servizio Notion**](notion-service.md) - Architettura modulare per integrazione Notion API
- **📊 Servizi Core** - Logica di business e orchestrazione *(da documentare)*

### 🛠️ Componenti Tecnici
- **⚙️ Configurazione** - Setup ambiente e parametri *(da documentare)*
- **🔄 Schedulazione** - Sistema di invio automatico notifiche *(da documentare)*
- **📝 Template System** - Gestione messaggi dinamici *(da documentare)*

### 🚀 Deployment & Operations
- **🐳 Docker** - Containerizzazione e deployment *(da documentare)*
- **📈 Monitoring** - Logging e metriche *(da documentare)*
- **🔐 Security** - Gestione token e permessi *(da documentare)*

---

## 🎯 Quick Start

### Panoramica del Sistema
Formazing è un sistema automatizzato che:
1. **Recupera** informazioni su formazioni aziendali da Notion
2. **Formatta** i dati secondo template configurabili 
3. **Invia** notifiche automatiche via Telegram ai gruppi appropriati
4. **Gestisce** comandi interattivi per consultazioni manuali

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
- **📝 PyYAML** - Gestione template messaggi
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
│   └── 🔗 notion-service.md     # Documentazione servizio Notion
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
- **Training Service** *(coming soon)* - Logica orchestrazione e business rules
- **Configuration Guide** *(coming soon)* - Setup completo ambiente

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