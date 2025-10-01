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

## 🔧 Best Practices per Pages

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

### Statistiche Sistema Completo
- **2 Pages** (login, dashboard)
- **2 Layouts** (base, auth_required)
- **4 Organisms** (stats, table, tabs, flash_messages)
- **3 Molecules** (stat_card, formazione_row, flash_message)
- **5 Atoms** (button, badge, card, icon, loading)

**Total: 16 componenti** nel sistema Atomic Design di Formazing! 🎨✨

---

## 🚀 Prossimi Passi

Con pages complete, hai ora il sistema Atomic Design completo! Puoi procedere con:

1. **[Template System Guide](template-system.md)** - Guida completa all'utilizzo
2. **[Components Reference](components-reference.md)** - Riferimento rapido
3. **[Development Workflow](development.md)** - Best practices sviluppo

Le pages rappresentano il culmine del design system - qui l'utente vive l'esperienza completa di Formazing! 📄🏆