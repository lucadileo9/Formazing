# 📚 Formazing - Documentazione

**Sistema di notifiche automatiche per formazioni aziendali tramite Telegram Bot**

## 📋 Indice Documentazione

### 🏗️ Architettura del Sistema
- [**🤖 Bot Telegram**](bot-telegram.md) - Sistema bot, comandi, formattazione messaggi
- [**🔗 Servizio Notion**](notion-service.md) - Architettura modulare per integrazione Notion API
- [**🧪 Testing & Quality**](testing/) - Sistema di test completo, fixture e validazione qualità
- [**📑 Templates**](templates/) - Guida all'UI dell'applicazione

### 📚 Guide Specializzate  
- **📊 Servizi Core** - Logica di business e orchestrazione *(da documentare)*
- **⚙️ Configurazione** - Setup ambiente, deployment, variabili *(da documentare)*
- **🔧 API Reference** - Endpoints Flask, parametri, esempi *(da documentare)*

---
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

```mermaid
graph TB
    %% Database e API esterne
    NotionDB[(Notion Database<br/>Formazioni)]
    MSGraph[Microsoft Graph API<br/>Email + Teams]
    TelegramAPI[Telegram Bot API]
    
    %% Core Backend
    Flask[Flask Backend<br/>routes.py]
    NotionService[NotionService<br/>5 moduli]
    TelegramService[TelegramService<br/>Bot + Commands]
    
    %% Configurazioni
    Config[Configurazioni<br/>YAML + JSON]
    Templates[Jinja Templates<br/>UI + Web]
    
    %% Flusso principale
    NotionDB --> NotionService
    NotionService --> Flask
    Flask --> TelegramService
    TelegramService --> TelegramAPI
    Flask --> MSGraph
    
    %% Configurazioni e UI
    Config --> TelegramService
    Config --> MSGraph
    Templates --> Flask
    
    %% Styling
    classDef external fill:#e1f5fe
    classDef core fill:#f3e5f5
    classDef config fill:#fff3e0
    
    class NotionDB,MSGraph,TelegramAPI external
    class Flask,NotionService,TelegramService core
    class Config,Templates config
```

**Componenti Principali:**
- **🔵 Servizi Esterni**: Notion (database), Microsoft Graph (email/Teams), Telegram Bot API
- **🟣 Core Backend**: Flask (orchestratore), NotionService (5 moduli), TelegramService (bot + comandi)  
- **🟠 Configurazione & UI**: File YAML/JSON (gruppi + template messaggi), Jinja Templates (web UI)

**Flusso Dati:**
1. **NotionService** recupera formazioni dal database Notion
2. **Flask** orchestra il workflow e gestisce la web UI con Jinja
3. **TelegramService** formatta e invia notifiche usando configurazioni YAML/JSON
4. **Microsoft Graph** gestisce email e meeting Teams

## 📊 Stack Tecnologico

### 🔧 Backend Core
- **🐍 Python 3.9+** - Linguaggio principale
- **🌐 Flask** - Web framework per dashboard e API
- **🎨 Jinja2** - Template engine per UI web
- **🔗 Notion SDK** - Integrazione database formazioni

### 🤖 Integrazione Bot & Notifiche  
- **📱 python-telegram-bot** - SDK Telegram Bot API
- **📧 Microsoft Graph API** - Email e calendari Outlook/Teams
- **📝 PyYAML** - Template messaggi e configurazioni gruppi

### 🧪 Quality & Testing
- **🎯 pytest** - Framework testing principale  
- **🔧 Fixture modulari** - 39 fixture specializzate per testing
- **⚡ Quick test scripts** - Automazione testing Windows/Linux

---