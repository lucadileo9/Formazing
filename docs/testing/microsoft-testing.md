# 🔷 Microsoft Teams Integration Testing

**Guida completa ai test del modulo Microsoft Teams per calendarizzazione formazioni**

---

## 📋 Indice

1. [Panoramica Sistema Test](#-panoramica-sistema-test)
2. [Architettura Test Microsoft](#-architettura-test-microsoft)
3. [Test Scripts Disponibili](#-test-scripts-disponibili)
4. [Comandi Quick Test](#-comandi-quick-test)
5. [Configurazione Richiesta](#-configurazione-richiesta)
6. [Workflow di Test](#-workflow-di-test)
7. [Troubleshooting](#-troubleshooting)

---

## 🎯 Panoramica Sistema Test

Il modulo Microsoft Teams è testato attraverso **2 script principali** che validano:

- ✅ **Autenticazione** Microsoft Graph API (OAuth2 Client Credentials)
- ✅ **Creazione eventi** calendario con Teams meeting automatico
- ✅ **Invio email** a mailing list configurate per area
- ✅ **Integrazione Notion** → Microsoft → Notion (workflow completo)
- ✅ **Aggiornamento database** Notion con link Teams e stato

**⚠️ Considerazione importante**: I test Microsoft **creano dati reali** nel calendario e inviano email reali. Usare con attenzione e validare sempre la configurazione email prima dell'esecuzione.

---

## 🏗️ Architettura Test Microsoft

### **Script di Test**

```
Formazing/
├── tests/
│   ├── unit/
│   │   └── test_microsoft_service.py          # Test validazione rapida (config, init)
│   ├── e2e/
│   │   └── test_real_microsoft.py             # Test isolato Microsoft Service
│   └── integration/
│       └── test_notion_microsoft_integration.py # Test integrazione completa
```

### **Moduli Testati**

```
app/services/microsoft/
├── __init__.py              # MicrosoftService (facade)
├── graph_client.py          # GraphClient (auth OAuth2)
├── email_formatter.py       # EmailFormatter (template YAML)
└── calendar_operations.py   # CalendarOperations (CRUD eventi)
```

### **Fixture e Mock**

A differenza di Notion e Telegram, il Microsoft Service **non ha fixture dedicate** perché:
- Richiede **credenziali reali** Graph API (impossibile mockare completamente)
- Le operazioni sono **atomiche** e reversibili (eventi eliminabili)
- I test sono **end-to-end** per natura (validano l'intera catena auth → API → response)

---

## 📝 Test Scripts Disponibili

### **1. test_real_microsoft.py** - Test Isolato (E2E)

**Percorso**: `tests/e2e/test_real_microsoft.py`

**Scopo**: Valida il Microsoft Service senza dipendenze da Notion.

**Cosa testa**:
- ✅ Configurazione variabili ambiente (`.env`)
- ✅ Autenticazione OAuth2 con Microsoft Graph API
- ✅ Creazione evento calendario con data futura (+5 minuti)
- ✅ Generazione automatica Teams meeting link
- ✅ Invio email a mailing list configurata (es. `lucadileo@jemore.it`)
- ✅ Validazione response: event ID, Teams link, calendar link

**Dati di test**:
```python
formazione_test = {
    'Nome': '🧪 TEST - Formazione Microsoft Integration',
    'Codice': 'TEST-MSFT-2024-01',
    'Data/Ora': '07/10/2025 14:30',  # +5 minuti da ora esecuzione
    'Area': ['Test']  # Modificabile per testare altre aree
}
```

**Sicurezza**:
- ⚠️ Richiede conferma esplicita "SI" (case-insensitive)
- 📊 Mostra preview completa prima dell'esecuzione
- 🔍 Valida configurazione prima di procedere
- ❌ Fallisce immediatamente se mancano credenziali

---

### **2. test_notion_microsoft_integration.py** - Test Integrazione

**Percorso**: `tests/integration/test_notion_microsoft_integration.py`

**Scopo**: Valida il workflow completo Notion → Microsoft → Notion.

**Cosa testa**:
- ✅ Recupero formazioni da Notion (stato "Programmata")
- ✅ Selezione interattiva formazione da calendarizzare
- ✅ Creazione evento Teams con dati reali da Notion
- ✅ Gestione multi-area (email a più mailing list)
- ✅ Aggiornamento atomico Notion: stato + link Teams

**Workflow step-by-step**:
```
1. 🔍 Verifica configurazione (Notion + Microsoft)
   ↓
2. 📚 Recupera formazioni "Programmata" da Notion
   ↓
3. 📝 Selezione interattiva formazione (o auto-select se unica)
   ↓
4. 📋 Mostra riepilogo operazione + email destinatari
   ↓
5. ⚠️ Richiede conferma "SI" con preview completo
   ↓
6. 📅 Crea evento Teams + genera meeting link
   ↓
7. 📧 Invia email a mailing list delle aree
   ↓
8. 🔄 Aggiorna Notion: Stato → "Calendarizzata", Link Teams salvato
   ↓
9. ✅ Verifica aggiornamento (ricarica da Notion)
   ↓
10. 🎉 Report finale con risultati
```

**Dati reali da Notion**:
```python
# Esempio formazione recuperata
{
    'Nome': 'Sicurezza Informatica Avanzata',
    'Codice': 'IT-Security-2024-SPRING-01',
    'Data/Ora': '15/10/2024 14:30',
    'Area': ['IT', 'R&D'],  
    'Stato': 'Programmata',
    '_notion_id': '12345678-90ab-cdef-1234-567890abcdef'
}
```
---

## 🚀 Comandi Quick Test

### **Test Isolato Microsoft Service**
```bash
# Windows
.\quick_test.bat microsoft

# Linux/Mac
./quick_test.sh microsoft

# Equivalente Python diretto
python tests/e2e/test_real_microsoft.py
```

**Quando usare**:
- ✅ Dopo modifiche a `app/services/microsoft/`
- ✅ Per validare autenticazione Graph API
- ✅ Per testare nuovo mapping area → email
- ✅ Prima di deploy se modifiche a template calendario

---

### **Test Integrazione Completa**
```bash
# Windows
.\quick_test.bat integration

# Linux/Mac
./quick_test.sh integration

# Equivalente Python diretto
python tests/integration/test_notion_microsoft_integration.py
```

**Quando usare**:
- ✅ Prima di deploy produzione (validazione end-to-end)
- ✅ Dopo modifiche a `training_service.py` (orchestratore)
- ✅ Per testare aggiornamento Notion + Microsoft
- ✅ Validazione workflow calendarizzazione completo

---

### **Suite Completa Microsoft**
```bash
# Windows
.\quick_test.bat teams

# Linux/Mac
./quick_test.sh teams
```

**Cosa fa**:
1. **Step 1** (opzionale con conferma): Test isolato Microsoft
2. **Step 2** (opzionale con conferma): Test integrazione Notion
3. **Report finale**: Riepilogo risultati entrambi i test

**Quando usare**:
- ✅ Validazione completa prima di merge branch `microsoft_integration`
- ✅ Prima di release con nuove funzionalità Microsoft
- ✅ Per troubleshooting completo Microsoft + Notion

---

## ⚙️ Configurazione Richiesta

### **1. Variabili Ambiente (.env)**

```env
# Microsoft Graph API - OAuth2 Client Credentials
MICROSOFT_TENANT_ID=your-azure-tenant-id
MICROSOFT_CLIENT_ID=your-app-registration-client-id
MICROSOFT_CLIENT_SECRET=your-client-secret-value
MICROSOFT_USER_EMAIL=organizer@domain.com  # Email organizzatore eventi
```


### **2. Mapping Aree → Email (config/microsoft_emails.json)**

```json
{
  "IT": "lucadileo@jemore.it",
  "HR": "hr@jemore.it",
  "R&D": "rd@jemore.it",
  "Marketing": "marketing@jemore.it",
  "Commerciale": "commerciale@jemore.it",
  "Legale": "legale@jemore.it",
  "Test": "lucadileo@jemore.it",
  "default": "formazioni@jemore.it"
}
```

**Regole**:
- **Chiave**: Nome area esattamente come in Notion (case-sensitive)
- **Valore**: Indirizzo email mailing list 
- **`default`**: Fallback se area non trovata (obbligatorio)
- **Multi-area**: Se formazione ha più aree, invia a tutte le email corrispondenti

### **3. Template Messaggi (config/calendar_templates.yaml)**

```yaml
calendar_event:
  subject: |
    {Nome}
  
  body: |
    🎓 Formazione Programmata
    
    📋 Codice: {Codice}
    📅 Data: {Data}
    🎯 Area: {Area}
    
    ---
    Per maggiori informazioni contattare il coordinatore della formazione.
```

**Variabili disponibili**:
- `{Nome}` - Nome formazione da Notion
- `{Codice}` - Codice univoco (es. IT-Security-2024-SPRING-01)
- `{Data}` - Data formattata in italiano (es. "Lunedì 15 Ottobre 2024 - 14:30")
- `{Area}` - Area o liste aree (es. "IT, R&D")

**Note**:
- ⚠️ Il **Teams link viene inserito automaticamente** da Outlook/Teams, non serve includerlo nel template
- 📝 Il corpo supporta **HTML** (conversione automatica `\n` → `<br>`)

---

## 🔄 Workflow di Test

### **Scenario 1: Sviluppo Feature Microsoft**
```bash
# 1. Durante sviluppo - test continuo
.\quick_test.bat unit          # Valida logica (se hai aggiunto unit test)

# 2. Prima commit - validazione isolata
.\quick_test.bat microsoft     # Test service in isolamento

# 3. Prima merge - validazione completa
.\quick_test.bat integration   # Test workflow end-to-end
```

### **Scenario 2: Pre-Deploy Produzione**
```bash
# 1. Suite completa sicura
.\quick_test.bat all           # Unit + E2E (no Microsoft)

# 2. Validazione Microsoft
.\quick_test.bat teams         # Entrambi i test Microsoft

# 3. (Opzionale) Workflow reale completo
.\quick_test.bat workflow-real # Include Microsoft + Telegram + Notion
```

### **Scenario 3: Debug Problemi Microsoft**
```bash
# 1. Verifica configurazione base
.\quick_test.bat check         # Valida .env e file config

# 2. Test autenticazione
.\quick_test.bat microsoft     # Se fallisce → problema credenziali

# 3. Test integrazione Notion
.\quick_test.bat integration   # Se fallisce → problema parsing dati Notion
```

## 📚 Riferimenti

- **[Microsoft Graph API Docs](https://learn.microsoft.com/en-us/graph/api/overview)** - Documentazione ufficiale API
- **[Calendar Events API](https://learn.microsoft.com/en-us/graph/api/resources/event)** - Creazione eventi
- **[Online Meetings API](https://learn.microsoft.com/en-us/graph/api/resources/onlinemeeting)** - Teams meetings
- **[OAuth2 Client Credentials](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-client-creds-grant-flow)** - Autenticazione

---

**Ultimo aggiornamento**: 7 Ottobre 2025  
**Versione**: 1.0.0 (Prima release Microsoft Integration)
