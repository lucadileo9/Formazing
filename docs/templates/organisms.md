# 🦠 Organisms - Sezioni Complete

Gli **Organisms** sono sezioni complete e funzionali dell'interfaccia che combinano molecules e atoms per creare blocchi autonomi di funzionalità. Rappresentano aree distinte della pagina con scopo specifico e comportamento complesso.

## 🎯 Filosofia degli Organisms

- **Autonomia**: Sezioni complete e auto-contenute
- **Funzionalità**: Implementano feature complete dell'applicazione
- **Composizione**: Orchestrano molecules e atoms insieme
- **Riutilizzabili**: Utilizzabili in diverse pagine e contesti

---

## 📈 Dashboard Stats - Statistiche Dashboard

**File**: `templates/organisms/dashboard_stats.html`

### Descrizione
Sezione completa delle statistiche principali della dashboard. Combina múltiple stat_cards in una griglia responsive con logica di caricamento, errori e aggiornamento automatico.

### Props Disponibili
| Prop | Tipo | Default | Descrizione |
|------|------|---------|-------------|
| `stats` | object | - | Oggetto statistiche formazioni (richiesto) |


### Esempi di Utilizzo

#### Dashboard Stats Standard
```html
{% include 'organisms/dashboard_stats.html' %}
{% set stats = formazioni_stats %}
```
**Risultato**: Griglia 4 colonne con stat cards per ogni status + totale


---

## 🧭 Tab Navigation - Navigazione Tab

**File**: `templates/organisms/tab_navigation.html`

### Descrizione
Sistema di navigazione a tab completo con supporto per filtri, contatori, icone e stato attivo. Gestisce la logica di switching e aggiornamento contenuti.

### Props Disponibili
| Prop | Tipo | Default | Descrizione |
|------|------|---------|-------------|
| `tabs` | array | - | Lista oggetti tab (richiesto) |

### Esempi di Utilizzo

#### Tab Navigation Standard
```html
{% include 'organisms/tab_navigation.html' %}
{% set tabs = formazioni_tabs %}
```


---

## 📋 Formazioni Table - Tabella Formazioni

**File**: `templates/organisms/formazioni_table.html`

### Descrizione
Tabella completa e responsive per visualizzare formazioni con sorting, paginazione, filtri avanzati e azioni bulk. Combina múltiple formazione_row molecules.

### Props Disponibili
| Prop | Tipo | Default | Descrizione |
|------|------|---------|-------------|
| `formazioni` | array | - | Lista formazioni (richiesto) |

### Esempi di Utilizzo

#### Tabella Standard
```html
{% include 'organisms/formazioni_table.html' %}
{% set formazioni = formazioni_list %}
```

---

## 💬 Flash Messages - Sistema Messaggi

**File**: `templates/organisms/flash_messages.html`

### Descrizione
Container completo per tutti i messaggi flash dell'applicazione con gestione automatica di múltipli messaggi, priorità e posizionamento.

### Props Disponibili
| Prop | Tipo | Default | Descrizione |
|------|------|---------|-------------|
| `messages` | array | - | Lista messaggi flash |

### Esempi di Utilizzo

#### Flash Messages Standard
```html
{% include 'organisms/flash_messages.html' %}
{% set messages = get_flashed_messages(with_categories=true) %}
```


### 🎯 Quando Usare Ciascun Organism

- **Dashboard Stats**: KPI overview, metrics summary, real-time statistics
- **Tab Navigation**: Content filtering, status switching, category browsing
- **Formazioni Table**: Data listing, bulk operations, detailed views
- **Flash Messages**: User feedback, operation results, system notifications

---

## 🚀 Prossimi Passi

Ora che hai padroneggiato organisms, molecules e atoms, puoi procedere con:

1. **[Pages](pages.md)** - Composizione finale (dashboard, login)
2. **[Layouts](layouts.md)** - Strutture di pagina (base, auth_required)
3. **[Template System](template-system.md)** - Guida completa al sistema

Gli organisms rappresentano le feature complete di Formazing - qui orchestri tutto il sistema atomico per creare funzionalità end-to-end! 🦠✨