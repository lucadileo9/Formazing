# 🏗️ Layouts - Strutture di Pagina

I **Layouts** sono le strutture fondamentali che definiscono l'architettura HTML delle pagine. Forniscono il framework base con head, body, risorse esterne e blocchi di contenuto riutilizzabili per tutte le pagine dell'applicazione.

## 🎯 Filosofia dei Layouts

- **Struttura Base**: Fondamenta HTML comuni a tutte le pagine
- **Ereditarietà**: Sistema gerarchico con extends/blocks Jinja2
- **Risorse Condivise**: CSS, JS e meta tags centralizzati
- **Modularità**: Blocchi specifici per diversi tipi di pagina

---

## �️ Base Layout - Struttura Fondamentale

**File**: `templates/layout/base.html`

### Descrizione
Layout principale dell'applicazione che fornisce la struttura HTML base, risorse Bootstrap, CSS personalizzato e blocchi fondamentali per tutte le pagine.

### Blocchi Disponibili
| Blocco | Scopo | Richiesto | Descrizione |
|--------|-------|-----------|-------------|
| `head` | Meta/CSS aggiuntivi | No | Risorse specifiche della pagina |
| `content` | Contenuto principale | Sì | Body principale della pagina |
| `scripts` | JavaScript | No | Script specifici della pagina |


### Caratteristiche Integrate

#### Risorse Bootstrap 5.3.0
- **CSS**: Framework responsive completo
- **Icons**: Bootstrap Icons 1.10.0 per iconografia
- **JavaScript**: Bundle completo con Popper.js

#### Meta Tags Responsive
- **Viewport**: Configurazione mobile-first
- **Charset**: UTF-8 per supporto internazionale
- **Language**: Italiano come lingua principale

#### Sistema Flash Messages
- **Automatico**: Incluso in tutte le pagine che estendono base
- **Posizionamento**: Top-level per visibilità massima

### Esempi di Utilizzo

#### Pagina Semplice
```html
{% extends "layout/base.html" %}

{% block content %}
<div class="container">
    <h1>Pagina Semplice</h1>
    <p>Contenuto della pagina</p>
</div>
{% endblock %}
```

#### Pagina con CSS Personalizzato
```html
{% extends "layout/base.html" %}

{% block head %}
<style>
.custom-gradient {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
</style>
{% endblock %}

{% block content %}
<div class="container-fluid vh-100 custom-gradient">
    <!-- Contenuto fullscreen -->
</div>
{% endblock %}
```

#### Pagina con JavaScript
```html
{% extends "layout/base.html" %}

{% block content %}
<div class="container">
    <button id="myButton">Click me</button>
</div>
{% endblock %}

{% block scripts %}
<script>
document.getElementById('myButton').addEventListener('click', function() {
    alert('Button clicked!');
});
</script>
{% endblock %}
```

### Configurazione Title Dinamico
```python
# Nel route Flask
@app.route('/dashboard')
def dashboard():
    return render_template('pages/dashboard.html', 
                         title='Dashboard - Formazing',
                         stats=stats)
```

---

## 🔐 Auth Required Layout - Pagine Protette

**File**: `templates/layout/auth_required.html`

### Descrizione
Layout specializzato per pagine che richiedono autenticazione. Estende il base layout aggiungendo un container centralizzato e padding standard per l'area di contenuto.

### Blocchi Disponibili
| Blocco | Scopo | Richiesto | Descrizione |
|--------|-------|-----------|-------------|
| `page_content` | Contenuto pagina | Sì | Contenuto all'interno del container |
| `head` | Meta/CSS aggiuntivi | No | Ereditato da base layout |
| `scripts` | JavaScript | No | Ereditato da base layout |

### Caratteristiche Integrate

#### Container Bootstrap
- **Responsive**: Si adatta automaticamente ai breakpoints
- **Padding Verticale**: `py-4` per spaziatura standard
- **Centrato**: Container Bootstrap centrato orizzontalmente

#### Ereditarietà Completa
- **Flash Messages**: Automaticamente inclusi dal base layout
- **Risorse**: Bootstrap CSS/JS, Bootstrap Icons, style.css
- **Meta Tags**: Configurazione mobile e SEO

### Esempi di Utilizzo

#### Dashboard Protetta
```html
{% extends "layout/auth_required.html" %}

{% block page_content %}
    <!-- Dashboard Header -->
    <div class="row mb-4">
        <div class="col">
            <h1 class="h2 fw-bold">Dashboard Formazioni</h1>
        </div>
    </div>

    <!-- Statistics Section -->
    {% include 'organisms/dashboard_stats.html' %}
    
    <!-- Content Section -->
    {% include 'organisms/formazioni_table.html' %}
{% endblock %}
```

#### Pagina Admin con Scripts
```html
{% extends "layout/auth_required.html" %}

{% block page_content %}
    <h1>Pannello Amministratore</h1>
    <div class="row">
        <!-- Admin content -->
    </div>
{% endblock %}

{% block scripts %}
<script>
// Auto-refresh per admin dashboard
setInterval(() => {
    refreshAdminStats();
}, 30000);
</script>
{% endblock %}
```

---

### 🎯 Quando Usare Ciascun Layout

#### **Base Layout** (`layout/base.html`)
- **Login/Landing pages** che necessitano layout fullscreen
- **Pagine pubbliche** senza autenticazione
- **Layout completamente personalizzati** (admin, reports)
- **Pagine con struttura speciale** (error pages, maintenance)

#### **Auth Required Layout** (`layout/auth_required.html`)
- **Dashboard** e pagine principali dell'app
- **Pagine CRUD** per gestione dati
- **Settings** e configurazioni utente
- **Reports** e analytics containerizzati

---

## �️ Architettura Gerarchica

```
layout/
├── base.html                 # Foundation layout
│   ├── HTML5 structure
│   ├── Bootstrap integration  
│   ├── Flash messages
│   └── Script/CSS blocks
│
└── auth_required.html         # Protected layout
    ├── extends base.html
    ├── Container wrapper (py-4)
    └── page_content block
```

---

## 🚀 Prossimi Passi

Ora che hai completato layouts, atoms, molecules e organisms, puoi procedere con:

1. **[Pages](pages.md)** - Composizione finale delle pagine
2. **[Template System Guide](template-system.md)** - Guida completa al sistema
3. **[Components Reference](components-reference.md)** - Riferimento rapido

I layouts sono la fondazione architettonica - tutto il sistema atomico si costruisce sopra questa base solida! 🏗️✨