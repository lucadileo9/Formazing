# 📚 Formazing - Documentazione

**Sistema di notifiche automatiche per formazioni aziendali tramite Telegram Bot**

## 📋 Indice Documentazione

### 🏗️ Architettura del Sistema
- [**🤖 Bot Telegram**](bot-telegram.md) - Sistema bot, comandi, formattazione messaggi
- [**🔗 Servizio Notion**](notion-service.md) - Architettura modulare per integrazione Notion API
- [**🧪 Testing & Quality**](testing/) - Sistema di test completo, fixture e validazione qualità

### 📚 Guide Specializzate  
- **📊 Servizi Core** - Logica di business e orchestrazione *(da documentare)*
- **⚙️ Configurazione** - Setup ambiente, deployment, variabili *(da documentare)*
- **🔧 API Reference** - Endpoints Flask, parametri, esempi *(da documentare)*

---

## 🎯 Quick Documentazione

### 📖 Per Sviluppatori
1. **[🤖 Sistema Bot](bot-telegram.md)** - Se lavori su comandi bot, formattazione messaggi
2. **[🔗 Notion Service](notion-service.md)** - Se lavori su integrazione database, query, parsing
3. **[🧪 Testing](testing/)** - Se lavori su test, fixture, validazione qualità

## 🎯 Quick Start

### Panoramica del Sistema
Formazing è un sistema automatizzato che:
1. **Recupera** informazioni su formazioni aziendali da Notion
2. **Formatta** i dati secondo template configurabili 
3. **Invia** notifiche automatiche via Telegram ai gruppi appropriati
4. **Calendarizza** eventi e invia email tramite Microsoft Graph API
5. **Gestisce** comandi interattivi per consultazioni manuali

---

## 🏗️ Architettura High-Level

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│   Notion API    │◄───┤  Flask Backend  │───►│ Telegram Bot    │
│   (Database)    │    │  (Orchestratore)│    │  (Notifiche)    │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Microsoft      │
                    │  Graph API      │
                    │ (Email + Teams) │
                    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Configurazione  │
                    │ (YAML + JSON)   │
                    └─────────────────┘
```

## 📊 Stack Tecnologico

### 🔧 Backend Core
- **🐍 Python 3.9+** - Linguaggio principale
- **🌐 Flask** - Web framework per dashboard e API
- **🔗 Notion SDK** - Integrazione database formazioni

### 🤖 Integrazione Bot & Notifiche  
- **📱 python-telegram-bot** - SDK Telegram Bot API
- **📧 Microsoft Graph API** - Email e calendari Outlook/Teams
- **📝 PyYAML** - Template messaggi configurabili

### 🧪 Quality & Testing
- **🎯 pytest** - Framework testing principale  
- **🔧 Fixture modulari** - 39 fixture specializzate per testing
- **⚡ Quick test scripts** - Automazione testing Windows/Linux

---

## 📞 Supporto e Contributi

### 🔍 Troubleshooting
- **Per errori di test**: [docs/testing/README.md](testing/README.md)
- **Per problemi bot**: [docs/bot-telegram.md](bot-telegram.md)
- **Per errori Notion**: [docs/notion-service.md](notion-service.md)
