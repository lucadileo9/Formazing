# 📄 Pages - Pagine Complete

Le **Pages** sono la composizione finale del sistema Atomic Design, dove tutti i componenti (atoms, molecules, organisms, layouts) si uniscono per creare esperienze utente complete e funzionali.

## 🎯 Filosofia delle Pages

- **Composizione Finale**: Orchestrano tutti i livelli del design system
- **User Experience**: Implementano flussi utente completi
- **Business Logic**: Integrano logica specifica dell'applicazione
- **Responsive**: Ottimizzate per tutti i dispositivi

---

## 🏠 Login Page - Pagina di Accesso

**File**: `templates/pages/login.html`

### Descrizione
Pagina di accesso pubblico con design fullscreen, gradient background e card centralizzata. Utilizza Basic Authentication del browser per l'accesso sicuro al sistema.

### Layout Utilizzato
Estende `layout/base.html` per layout completamente personalizzato senza container.

### Componenti Integrati
- **Atoms**: `icon.html`, `button.html`
- **Layout**: Fullscreen con gradient CSS
- **Bootstrap**: Card, grid system, utilities

### Caratteristiche Principali
- **Design Fullscreen**: Viewport 100% altezza
- **Gradient Background**: CSS personalizzato blu-viola
- **Card Centralizzata**: Shadow e border-radius
- **Responsive**: Mobile-first design
- **Basic Auth**: Integrazione browser nativa

### Esempi di Utilizzo

#### Accesso Standard
```html
{% extends "layout/base.html" %}

{% block content %}
<!-- Fullscreen container con gradient -->
<div class="container-fluid vh-100 d-flex align-items-center justify-content-center bg-gradient">
    <!-- Login card centrata -->
    <div class="card shadow-lg border-0">
        <!-- Icona shield-lock -->
        <!-- Titolo app -->
        <!-- Alert informativo -->
        <!-- Bottone accesso -->
    </div>
</div>
{% endblock %}
```

#### Con Title Personalizzato
```python
# Nel route Flask
@app.route('/login')
def login():
    return render_template('pages/login.html', 
                         app_name='Formazing Pro')
```

#### Con Scripts di Redirect
```html
{% block scripts %}
<script>
// Auto-redirect se già autenticato
document.addEventListener('DOMContentLoaded', function() {
    // Logic redirect
});
</script>
{% endblock %}
```

### Props Template
| Prop | Tipo | Default | Descrizione |
|------|------|---------|-------------|
| `app_name` | string | `'Formazing'` | Nome applicazione nel titolo |
| `title` | string | - | Title HTML personalizzato |

---

## 📊 Dashboard Page - Pagina Principale

**File**: `templates/pages/dashboard.html`

### Descrizione
Pagina principale dell'applicazione con statistiche, navigazione a tab e tabelle formazioni. Implementa il cuore funzionale del sistema di gestione formazioni.

### Layout Utilizzato
Estende `layout/auth_required.html` per pagine protette con container automatico.

### Componenti Integrati
- **Atoms**: `icon.html`, `button.html`
- **Organisms**: `dashboard_stats.html`, `formazioni_table.html`
- **Bootstrap**: Tabs, cards, alerts
- **JavaScript**: Auto-refresh, tab switching

### Caratteristiche Principali
- **Header con Icona**: Titolo dashboard con speedometer icon
- **Statistics Section**: Cards KPI con organisms
- **Tab Navigation**: 3 tab per status formazioni
- **Dynamic Content**: Contenuto cambia per tab
- **Empty States**: Messaggi quando non ci sono dati
- **Auto-refresh**: JavaScript per aggiornamenti automatici

### Blocchi Template
| Blocco | Scopo | Contenuto |
|--------|-------|-----------|
| `page_content` | Contenuto principale | Header + stats + tabs |
| `scripts` | JavaScript | Auto-refresh + tab logic |

### Esempi di Utilizzo

#### Dashboard Standard
```python
# Nel route Flask
@app.route('/dashboard')
async def dashboard():
    # Carica stats e formazioni
    return render_template('pages/dashboard.html',
                         stats=formazioni_stats,
                         formazioni_programmata=prog_list,
                         formazioni_calendarizzata=cal_list,
                         formazioni_conclusa=conc_list)
```

#### Con Auto-refresh Personalizzato
```html
{% block scripts %}
<script>
// Custom refresh interval
let autoRefreshInterval = setInterval(() => {
    refreshDashboard();
}, {{ refresh_interval|default(60000) }});
</script>
{% endblock %}
```

#### Con Filtri Aggiuntivi
```python
# Route con filtri
@app.route('/dashboard/<string:filter>')
async def dashboard_filtered(filter):
    # Applica filtro specifico
    return render_template('pages/dashboard.html',
                         current_filter=filter,
                         **data)
```

### Props Template
| Prop | Tipo | Descrizione |
|------|------|-------------|
| `stats` | object | Statistiche formazioni (total, programmata, etc.) |
| `formazioni_programmata` | array | Lista formazioni programmate |
| `formazioni_calendarizzata` | array | Lista formazioni calendarizzate |
| `formazioni_conclusa` | array | Lista formazioni concluse |
| `title` | string | Title HTML personalizzato |

### Struttura Tab Content
```html
<!-- Tab 1: Programmate -->
- Alert warning con info
- Organisms formazioni_table o empty state

<!-- Tab 2: Calendarizzate -->  
- Alert info con descrizione
- Organisms formazioni_table o empty state

<!-- Tab 3: Concluse -->
- Alert success con completamento
- Organisms formazioni_table o empty state
```

### Empty States per Tab
- **Programmate**: Icon check-circle-fill + "Nessuna formazione da programmare"
- **Calendarizzate**: Icon calendar-x + "Nessuna formazione calendarizzata"  
- **Concluse**: Icon hourglass + "Nessuna formazione conclusa"

---

## � Preview Page - Pagina Anteprima Azioni

**File**: `templates/pages/preview.html`

### Descrizione
Pagina di conferma/anteprima che mostra tutti i dettagli prima di eseguire azioni critiche (invio notifiche, richieste feedback). Compone tutte le molecole preview per un'esperienza UX completa e sicura.

### Layout Utilizzato
Estende `layout/base.html` con container standard.

### Componenti Integrati
- **Molecules**: 
  - `preview_training_info.html` - Dettagli formazione
  - `preview_telegram_messages.html` - Messaggi da inviare
  - `preview_email_section.html` - Email da inviare (solo notification)
  - `preview_action_form.html` - Riepilogo + bottoni conferma
- **Bootstrap**: Breadcrumb, cards, responsive grid
- **Custom CSS**: Hover effects, code selection

### Caratteristiche Principali
- **Breadcrumb navigation**: Dashboard → Preview
- **Header dinamico**: Titolo e icona cambiano per action_type
- **Composizione modulare**: 4 molecole preview stacked
- **Conferma sicura**: Alert JavaScript prima del submit
- **Responsive**: Mobile-first layout
- **Hover effects**: Cards con animazione subtle

### Parametri Template
| Prop | Tipo | Descrizione |
|------|------|-------------|
| `title` | string | Title HTML della pagina |
| `action_title` | string | Titolo visualizzato (es. "Preview Notifica") |
| `action_icon` | string | Emoji/icon per header (📨, 📝, etc.) |
| `action_type` | string | `'notification'` o `'feedback'` |
| `training_id` | string | ID Notion formazione |
| `preview` | object | Oggetto con `training`, `messages`, `email`, `codice_generato` |

### Struttura Preview Object
```python
preview = {
    'training': {
        'Nome': 'Corso Python Avanzato',
        'Area': ['IT', 'R&D'],
        'Data/Ora': '15/10/2025 15:00',
        'Stato': 'Programmata',
        'LinkTeams': 'https://teams.microsoft.com/...'
    },
    'messages': [
        {
            'area': 'IT',
            'chat_id': '-1001234567890', # Solo per debug, non mostrato
            'message': 'Formazione Python\nDomani ore 15:00'
        }
    ],
    'email': {  # Solo per notification
        'recipients': ['team@company.com'],
        'subject': 'Invito: Formazione Python',
        'body_preview': 'Gentile partecipante...'
    },
    'codice_generato': 'IT-Python-2024-AUTUMN-03'  # Solo per notification
}
```

### Esempi di Utilizzo

#### Preview Notification
```python
# Nel route Flask
@app.route('/preview/notification/<training_id>')
async def preview_notification(training_id):
    # Prepara preview data
    preview_data = await prepare_notification_preview(training_id)
    
    return render_template(
        'pages/preview.html',
        title='Preview Notifica - Formazing',
        action_title='Preview Notifica Formazione',
        action_icon='📨',
        action_type='notification',
        training_id=training_id,
        preview=preview_data
    )
```

#### Preview Feedback
```python
@app.route('/preview/feedback/<training_id>')
async def preview_feedback(training_id):
    preview_data = await prepare_feedback_preview(training_id)
    
    return render_template(
        'pages/preview.html',
        title='Preview Richiesta Feedback - Formazing',
        action_title='Preview Richiesta Feedback',
        action_icon='📝',
        action_type='feedback',
        training_id=training_id,
        preview=preview_data
    )
```

### User Flow
```
1. User clicca "Invia Notifica" da dashboard
   ↓
2. Backend prepara preview data
   ↓
3. Preview page mostra tutti i dettagli
   ↓
4. User verifica informazioni
   ↓
5a. User clicca "Annulla" → torna dashboard
5b. User clicca "Conferma" → alert JS → POST confirm route
   ↓
6. Backend esegue azioni reali
   ↓
7. Redirect dashboard con flash message
```

### Differenze Notification vs Feedback

| Feature | Notification | Feedback |
|---------|-------------|----------|
| **Codice generato** | ✅ Mostra nuovo codice | ❌ Nascosto |
| **Email section** | ✅ Mostra card email | ❌ Nascosto |
| **Azioni alert** | 5 azioni | 2 azioni |
| **Stato finale** | Calendarizzata | Conclusa |
| **Icon** | 📨 | 📝 |

---

## �🔧 Best Practices per Pages

### ✅ Do (Fai così)
```html
<!-- ✅ Estendi il layout appropriato -->
{% extends "layout/auth_required.html" %}  <!-- Per dashboard -->
{% extends "layout/base.html" %}          <!-- Per login -->

<!-- ✅ Componi organisms per funzionalità -->
{% include 'organisms/dashboard_stats.html' %}
{% include 'organisms/formazioni_table.html' %}

<!-- ✅ Usa props per personalizzazione -->
{% set stats = formazioni_stats %}
{% set formazioni = current_list %}

<!-- ✅ Implementa empty states -->
{% if not formazioni %}
    <div class="text-center py-5">
        <!-- Empty state content -->
    </div>
{% endif %}
```

### ❌ Don't (Non fare così)
```html
<!-- ❌ Non duplicare logica organisms -->
<div class="stat-card">...</div>  <!-- Usa organisms invece -->

<!-- ❌ Non hardcodare contenuti -->
<h1>Dashboard Formazioni</h1>  <!-- Usa title prop -->

<!-- ❌ Non mescolare responsabilità -->
{% block content %}
    <!-- HTML + Business Logic -->  <!-- Separa in organisms -->
{% endblock %}
```

### 🎯 Quando Creare Nuove Pages

#### **Crea Page quando:**
- **Nuovo flusso utente** completo (es. settings, reports)
- **Diversa struttura layout** (es. fullscreen vs container)
- **Logica business distinta** (es. admin vs user)
- **Pattern navigation diverso** (es. wizard vs dashboard)

#### **Non creare Page quando:**
- **Variazione minore** di page esistente (usa props/routing)
- **Solo contenuto diverso** (usa template variables)
- **Stesso layout e organisms** (usa parametri URL)

---

## 🚀 Pattern di Composizione

### Page Architecture
```
pages/dashboard.html
├── layout/auth_required.html
│   └── layout/base.html (Bootstrap + resources)
├── organisms/dashboard_stats.html
│   └── molecules/stat_card.html
│       └── atoms/icon.html, atoms/card.html
├── organisms/formazioni_table.html  
│   └── molecules/formazione_row.html
│       └── atoms/badge.html, atoms/button.html
└── JavaScript auto-refresh logic
```

### Data Flow
```python
# Route → Template → Organisms → Molecules → Atoms
@app.route('/dashboard')
async def dashboard():
    data = await load_formazioni()  # Business logic
    return render_template('pages/dashboard.html', **data)
```

---

## 📊 Pages Summary

| Page | Layout | Scopo | Componenti Chiave |
|------|--------|-------|-------------------|
| `login.html` | `base.html` | Accesso pubblico | Icon, Button, Gradient CSS |
| `dashboard.html` | `auth_required.html` | Dashboard principale | Stats, Table, Tabs, Auto-refresh |
| `preview.html` | `base.html` | Conferma azioni critiche | 4 molecules preview, Breadcrumb, Dynamic content |

### Statistiche Sistema Completo
- **3 Pages** (login, dashboard, preview)
- **2 Layouts** (base, auth_required)
- **4 Organisms** (stats, table, tabs, flash_messages)
- **7 Molecules** (stat_card, formazione_row, flash_message, 4x preview molecules)
- **6 Atoms** (button, badge, card, icon, loading, telegram_message_preview)

**Total: 22 componenti** nel sistema Atomic Design di Formazing! 🎨✨

---

## 🚀 Prossimi Passi

Con pages complete, hai ora il sistema Atomic Design completo! Puoi procedere con:

1. **[Template System Guide](template-system.md)** - Guida completa all'utilizzo
2. **[Components Reference](components-reference.md)** - Riferimento rapido
3. **[Development Workflow](development.md)** - Best practices sviluppo

Le pages rappresentano il culmine del design system - qui l'utente vive l'esperienza completa di Formazing! 📄🏆