# 🧬 Molecules - Componenti Intelligenti

Le **Molecules** sono combinazioni funzionali di atoms che implementano logica di business specifica. Rappresentano blocchi di interfaccia riutilizzabili con comportamenti intelligenti e sono il ponte tra gli atoms puramente presentazionali e gli organisms complessi.

## 🎯 Filosofia delle Molecules

- **Business Logic**: Contengono logica specifica dell'applicazione
- **Composizione**: Combinano múltipli atoms in unità funzionali
- **Riutilizzabili**: Utilizzabili in diversi contesti e organisms
- **Intelligenti**: Prendono decisioni basate sui dati ricevuti

---

## 📊 Stat Card - Carta Statistica

**File**: `templates/molecules/stat_card.html`

### Descrizione
Card specializzata per visualizzare statistiche numeriche con icona, titolo, valore e descrizione. Include logica automatica per colorazione e formattazione basata sul tipo di statistica.

### Props Disponibili
| Prop | Tipo | Default | Descrizione |
|------|------|---------|-------------|
| `title` | string | - | Titolo della statistica (richiesto) |
| `value` | string/number | - | Valore numerico da mostrare (richiesto) |
| `icon` | string | `'bi bi-bar-chart'` | Icona Bootstrap Icons |
| `description` | string | - | Descrizione opzionale sotto il valore |
| `color` | string | `'text-primary'` | Colore dell'icona e accenti |
| `bg_class` | string | `''` | Classe background per la card |

### Logica Integrata
- **Auto-formattazione**: Numeri grandi vengono formattati (es. 1.2K, 3.4M)
- **Colorazione intelligente**: Colori diversi per tipi di statistiche
- **Responsive**: Si adatta automaticamente su mobile

### Esempi di Utilizzo

#### Statistica Semplice
```html
{% include 'molecules/stat_card.html' %}
{% set title = 'Totale Formazioni' %}
{% set value = formazioni_stats.total %}
{% set icon = 'bi bi-collection' %}
```
**Risultato**: Card con icona, "Totale Formazioni", numero grande al centro

#### Statistica con Descrizione
```html
{% include 'molecules/stat_card.html' %}
{% set title = 'Programmate' %}
{% set value = formazioni_stats.programmata %}
{% set icon = 'bi bi-clock-history' %}
{% set description = 'In fase di pianificazione' %}
{% set color = 'text-warning' %}
```

#### Statistica con Background Colorato
```html
{% include 'molecules/stat_card.html' %}
{% set title = 'Concluse' %}
{% set value = formazioni_stats.conclusa %}
{% set icon = 'bi bi-check-circle' %}
{% set description = 'Formazioni completate' %}
{% set color = 'text-white' %}
{% set bg_class = 'bg-success' %}
```

#### Griglia di Statistiche Dashboard
```html
<div class="row">
    <div class="col-md-3">
        {% include 'molecules/stat_card.html' %}
        {% set title = 'Totale' %}
        {% set value = stats.total %}
        {% set icon = 'bi bi-collection' %}
        {% set color = 'text-primary' %}
    </div>
    <div class="col-md-3">
        {% include 'molecules/stat_card.html' %}
        {% set title = 'Programmate' %}
        {% set value = stats.programmata %}
        {% set icon = 'bi bi-clock-history' %}
        {% set color = 'text-warning' %}
    </div>
    <div class="col-md-3">
        {% include 'molecules/stat_card.html' %}
        {% set title = 'Calendarizzate' %}
        {% set value = stats.calendarizzata %}
        {% set icon = 'bi bi-calendar-event' %}
        {% set color = 'text-info' %}
    </div>
    <div class="col-md-3">
        {% include 'molecules/stat_card.html' %}
        {% set title = 'Concluse' %}
        {% set value = stats.conclusa %}
        {% set icon = 'bi bi-check-circle' %}
        {% set color = 'text-success' %}
    </div>
</div>
```

### Mappature Automatiche Colori
```python
# Colori standard per status formazioni
status_colors = {
    'programmata': 'text-warning',
    'calendarizzata': 'text-info', 
    'conclusa': 'text-success',
    'total': 'text-primary'
}

# Icone standard per status
status_icons = {
    'programmata': 'bi bi-clock-history',
    'calendarizzata': 'bi bi-calendar-event',
    'conclusa': 'bi bi-check-circle',
    'total': 'bi bi-collection'
}
```

N.B.: queste mappature possono essere estese o sovrascritte passando props custom, oppure modificando i dizionari nel codice stesso.
N.B.: se venisse passata una configurazione diversa da quelle predefinite (programmata, calendarizzata, conclusa, total), il sistema utilizzerà le nuove impostazioni.
verranno utilizzati i valori di "total".

---

## 📋 Formazione Row - Riga Formazione

**File**: `templates/molecules/formazione_row.html`

### Descrizione
Riga specializzata per tabelle formazioni con logica integrata per badge status, formattazione date, azioni contestuali e colorazione automatica.

### Props Disponibili
| Prop | Tipo | Default | Descrizione |
|------|------|---------|-------------|
| `formazione` | object | - | Oggetto formazione da Notion (richiesto) |
| `show_actions` | boolean | `true` | Mostra colonna azioni |
| `compact` | boolean | `false` | Layout compatto per mobile |
| `highlight_status` | string | - | Status da evidenziare |

### Logica Integrata
- **Badge automatici**: Status e Area con colori predefiniti
- **Formattazione date**: Date in formato italiano leggibile
- **Azioni contestuali**: Bottoni diversi per ogni status
- **Responsiveness**: Nascondi/mostra colonne su mobile

### Struttura Dati Formazione
```python
formazione = {
    'id': 'notion_page_id',
    'Titolo': 'Corso Python Avanzato',
    'Area': 'IT',  # IT, HR, Marketing, etc.
    'Status': 'Programmata',  # Programmata, Calendarizzata, Conclusa
    'Data': '2025-10-15 15:00',
    'Periodo': 'AUTUMN',  # SPRING, AUTUMN, ONCE
}
```

### Esempi di Utilizzo

#### Riga Standard
```html
<tbody>
    {% for formazione in formazioni %}
        {% include 'molecules/formazione_row.html' %}
        {% set formazione = formazione %}
    {% endfor %}
</tbody>
```

#### Riga Compatta per Mobile
```html
{% include 'molecules/formazione_row.html' %}
{% set formazione = formazione %}
{% set compact = true %}
{% set show_actions = false %}
```

#### Riga con Evidenziazione
```html
{% include 'molecules/formazione_row.html' %}
{% set formazione = formazione %}
{% set highlight_status = 'Programmata' %}
```

### Mappature Badge Automatiche

#### Colori Area
```python
area_colors = {
    'IT': 'bg-primary',
    'HR': 'bg-success', 
    'Marketing': 'bg-warning',
    'Finance': 'bg-info',
    'Operations': 'bg-secondary'
}
```

#### Colori Status
```python
status_colors = {
    'Programmata': 'bg-warning',
    'Calendarizzata': 'bg-info',
    'Conclusa': 'bg-success'
}
```

#### Colori Periodo
```python
periodo_colors = {
    'SPRING': 'bg-light text-dark',
    'AUTUMN': 'bg-warning', 
    'ONCE': 'bg-info'
}
```

### Azioni Contestuali per Status
```html
<!-- Programmata: Pianifica -->
{% if formazione.Status == 'Programmata' %}
    {% include 'atoms/button.html' %}
    {% set text = 'Pianifica' %}
    {% set variant = 'btn-outline-warning' %}
    {% set size = 'btn-sm' %}
    {% set icon = 'bi bi-calendar-plus' %}

<!-- Calendarizzata: Avvia -->
{% elif formazione.Status == 'Calendarizzata' %}
    {% include 'atoms/button.html' %}
    {% set text = 'Avvia' %}
    {% set variant = 'btn-outline-info' %}
    {% set size = 'btn-sm' %}
    {% set icon = 'bi bi-play' %}

<!-- Conclusa: Report -->
{% elif formazione.Status == 'Conclusa' %}
    {% include 'atoms/button.html' %}
    {% set text = 'Report' %}
    {% set variant = 'btn-outline-success' %}
    {% set size = 'btn-sm' %}
    {% set icon = 'bi bi-file-text' %}
{% endif %}
```

### Responsive Behavior
```html
<!-- Desktop: Tutte le colonne -->
<td class="d-none d-md-table-cell">{{ formazione.get('Area', 'N/A') }}</td>
<td class="d-none d-lg-table-cell">{{ formazione.get('Periodo', 'N/A') }}</td>

<!-- Mobile: Solo info essenziali -->
<td class="d-md-none">
    <small class="text-muted">
        {{ formazione.get('Area', 'N/A') }} • {{ formazione.get('Periodo', 'N/A') }}
    </small>
</td>
```

---

## 💬 Flash Message - Messaggio Flash

**File**: `templates/molecules/flash_message.html`

### Descrizione
Componente per messaggi di feedback utente con chiusura automatica, icone appropriate e animazioni. Supporta diversi tipi di messaggio (successo, errore, warning, info).

### Props Disponibili
| Prop | Tipo | Default | Descrizione |
|------|------|---------|-------------|
| `message` | string | - | Testo del messaggio (richiesto) |


### Esempi di Utilizzo

#### Messaggio di Successo
```html
{% include 'molecules/flash_message.html' %}
{% set message = 'Formazione salvata con successo!' %}
{% set type = 'success' %}
```
**Risultato**: Alert verde con icona check, si chiude automaticamente

#### Messaggio di Errore
```html
{% include 'molecules/flash_message.html' %}
{% set message = 'Errore durante il salvataggio. Riprova.' %}
{% set type = 'error' %}
```


#### Integrazione Flask Flash Messages
```python
# Nel route Flask
from flask import flash

@app.route('/save_formazione', methods=['POST'])
async def save_formazione():
    try:
        # ... logica salvataggio ...
        flash('Formazione salvata con successo!', 'success')
    except Exception as e:
        flash(f'Errore: {str(e)}', 'error')
    
    return redirect(url_for('dashboard'))
```

```html
<!-- Nel template -->
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
            {% include 'molecules/flash_message.html' %}
            {% set message = message %}
            {% set type = category %}
            {% set auto_dismiss = true %}
        {% endfor %}
    {% endif %}
{% endwith %}
```

### Mappature Automatiche

#### Tipi → Bootstrap Classes
```python
type_mappings = {
    'success': 'alert-success',
    'error': 'alert-danger', 
    'warning': 'alert-warning',
    'info': 'alert-info'
}
```

#### Tipi → Icone
```python
icon_mappings = {
    'success': 'bi bi-check-circle',
    'error': 'bi bi-exclamation-triangle',
    'warning': 'bi bi-exclamation-circle', 
    'info': 'bi bi-info-circle'
}
```
---

### 🎯 Quando Usare Ciascuna Molecule

- **Stat Card**: KPI, metriche, contatori, dashboard statistics
- **Formazione Row**: Liste formazioni, tabelle dati, export reports
- **Flash Message**: Feedback utente, conferme operazioni, errori system

---

## 🚀 Prossimi Passi

Ora che hai padroneggiato molecules e atoms, puoi procedere con:

1. **[Organisms](organisms.md)** - Sezioni complete (dashboard_stats, formazioni_table)
2. **[Templates/Pages](pages.md)** - Composizione finale (dashboard, login)
3. **[Layouts](layouts.md)** - Strutture di pagina (base, auth_required)

Le molecules sono il cuore del business logic - qui implementi le regole e i comportamenti specifici di Formazing! 🧬✨