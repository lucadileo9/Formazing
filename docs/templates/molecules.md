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

## 📋 Preview Training Info - Card Informazioni Formazione

**File**: `templates/molecules/preview_training_info.html`

### Descrizione
Card macro che mostra tutte le informazioni chiave di una formazione nelle pagine di preview/conferma. Include dettagli formazione, badges area, stato attuale e codice generato.

### Macro Signature
```jinja
{% macro training_info_card(training, action_type, codice_generato=None) %}
```

### Parametri
| Param | Tipo | Default | Descrizione |
|-------|------|---------|-------------|
| `training` | object | - | Oggetto formazione da Notion (richiesto) |
| `action_type` | string | - | Tipo azione: `'notification'` o `'feedback'` |
| `codice_generato` | string | `None` | Codice univoco generato (solo per notification) |

### Logica Integrata
- **Badge dinamici**: Usa `atoms/badge.html` per Area e Stato
- **Condizionale codice**: Mostra "Nuovo Codice" se `action_type == 'notification'`
- **Link Teams**: Visualizza link meeting se presente
- **Formattazione date**: Data/Ora formattata automaticamente

### Esempi di Utilizzo

#### Preview Notifica (con codice generato)
```html
{% from 'molecules/preview_training_info.html' import training_info_card %}

{{ training_info_card(
    training=formazione,
    action_type='notification',
    codice_generato='IT-Security-2024-SPRING-01'
) }}
```
**Risultato**: Card con Nome, Area badges, Data, Stato, **Nuovo Codice**, Link Teams

#### Preview Feedback
```html
{% from 'molecules/preview_training_info.html' import training_info_card %}

{{ training_info_card(
    training=formazione,
    action_type='feedback'
) }}
```
**Risultato**: Card con Nome, Area badges, Data, Stato, Codice esistente (se presente)

### Struttura Training Object
```python
training = {
    'Nome': 'Corso Python Avanzato',
    'Area': ['IT', 'R&D'],  # Array per multiple aree
    'Data/Ora': '15/10/2025 15:00',
    'Stato': 'Programmata',  # Programmata | Calendarizzata | Conclusa
    'Codice': 'IT-Python-2024-AUTUMN-03',  # Opzionale
    'LinkTeams': 'https://teams.microsoft.com/...'  # Opzionale
}
```

### Badge Automatici
- **Area badges**: `bg-secondary` per ogni area nell'array
- **Stato badge**:
  - `Programmata` → `bg-warning`
  - `Calendarizzata` → `bg-info`
  - `Conclusa` → `bg-success`

---

## 📨 Preview Telegram Messages - Card Messaggi Telegram

**File**: `templates/molecules/preview_telegram_messages.html`

### Descrizione
Card macro che visualizza l'anteprima di tutti i messaggi Telegram che verranno inviati, organizzati per area/gruppo target.

### Macro Signature
```jinja
{% macro telegram_messages_card(messages) %}
```

### Parametri
| Param | Tipo | Default | Descrizione |
|-------|------|---------|-------------|
| `messages` | array | - | Lista messaggi con area, chat_id, message (richiesto) |

### Logica Integrata
- **Conteggio gruppi**: Badge con numero totale gruppi target
- **Preview messaggi**: Usa `atoms/telegram_message_preview.html` per ogni messaggio
- **Empty state**: Alert warning se `messages` è vuoto
- **Layout verticale**: Stack di cards con gap

### Esempi di Utilizzo

#### Con Messaggi
```html
{% from 'molecules/preview_telegram_messages.html' import telegram_messages_card %}

{{ telegram_messages_card(messages=telegram_messages) }}
```

#### Struttura Messages Array
```python
telegram_messages = [
    {
        'area': 'IT',
        'chat_id': '-1001234567890',
        'message': 'Formazione Python\nDomani ore 15:00\n\nLink: https://...'
    },
    {
        'area': 'HR',
        'chat_id': '-1009876543210', 
        'message': 'Reminder Leadership training\nOggi pomeriggio alle 14:30'
    }
]
```

### Empty State
```html
<!-- Se messages è vuoto o None -->
<div class="alert alert-warning">
    <i class="bi bi-exclamation-triangle"></i>
    <strong>Attenzione!</strong> Nessun messaggio da inviare.
</div>
```

---

## 📧 Preview Email Section - Sezione Email

**File**: `templates/molecules/preview_email_section.html`

### Descrizione
Card macro per visualizzare l'anteprima dell'email che verrà inviata con dettagli meeting Teams. Mostrata solo se email presente.

### Macro Signature
```jinja
{% macro email_section_card(email) %}
```

### Parametri
| Param | Tipo | Default | Descrizione |
|-------|------|---------|-------------|
| `email` | object/None | - | Oggetto email con recipients, subject, body_preview |

### Logica Integrata
- **Rendering condizionale**: Card mostrata solo se `email` è truthy
- **Destinatari multipli**: Join con virgola
- **Body preview**: Anteprima testo email in box grigio

### Esempi di Utilizzo

#### Con Email
```html
{% from 'molecules/preview_email_section.html' import email_section_card %}

{{ email_section_card(email=email_data) }}
```

#### Struttura Email Object
```python
email_data = {
    'recipients': ['team@company.com', 'manager@company.com'],
    'subject': 'Invito: Formazione Python Avanzato - 15/10/2025',
    'body_preview': 'Gentile partecipante, sei invitato alla formazione...'
}
```

#### Senza Email (non renderizza nulla)
```html
{{ email_section_card(email=None) }}
<!-- Output: nessun HTML -->
```

### Caratteristiche
- **Card header verde**: `bg-success` per indicare email
- **Icon envelope**: `bi bi-envelope` nel header
- **Recipients list**: Separati da virgola
- **Preview box**: `bg-light` con padding

---

## ⚡ Preview Action Form - Form Azioni Finali

**File**: `templates/molecules/preview_action_form.html`

### Descrizione
Macro che renderizza il riepilogo azioni, alert di conferma e i due bottoni finali (Annulla/Conferma). Cuore della UX di conferma operazioni.

### Macro Signature
```jinja
{% macro action_form(action_type, training_id, codice_generato, messages_count) %}
```

### Parametri
| Param | Tipo | Default | Descrizione |
|-------|------|---------|-------------|
| `action_type` | string | - | `'notification'` o `'feedback'` (richiesto) |
| `training_id` | string | - | ID Notion della formazione (richiesto) |
| `codice_generato` | string | - | Codice univoco generato (solo notification) |
| `messages_count` | int | - | Numero gruppi Telegram (richiesto) |

### Logica Integrata
- **Lista azioni dinamica**: Diversa per notification vs feedback
- **Badge stato**: Usa `atoms/badge.html` per stati Notion
- **Conferma JavaScript**: Alert nativo browser prima submit
- **Bottoni con atoms**: Usa `atoms/button.html` per entrambi i button

### Esempi di Utilizzo

#### Per Notification
```html
{% from 'molecules/preview_action_form.html' import action_form %}

{{ action_form(
    action_type='notification',
    training_id=formazione.id,
    codice_generato='IT-Security-2024-SPRING-01',
    messages_count=3
) }}
```
**Azioni visualizzate:**
- ✅ Generazione codice univoco
- ✅ Creazione evento Teams Calendar
- ✅ Aggiornamento Notion: Stato → `Calendarizzata`
- ✅ Invio email con allegato Teams
- ✅ Invio messaggi Telegram a 3 gruppi

#### Per Feedback
```html
{{ action_form(
    action_type='feedback',
    training_id=formazione.id,
    codice_generato=None,
    messages_count=2
) }}
```
**Azioni visualizzate:**
- ✅ Invio richiesta feedback Telegram a 2 gruppi
- ✅ Aggiornamento Notion: Stato → `Conclusa`

### Bottoni

#### Bottone Annulla (sinistra)
```html
{% set text = 'Annulla e Torna alla Dashboard' %}
{% set icon = 'bi bi-x-circle' %}
{% set variant = 'btn-secondary' %}
{% set size = 'btn-lg w-100' %}
{% set onclick = "window.location.href='/dashboard'" %}
{% include 'atoms/button.html' %}
```

#### Bottone Conferma (destra)
```html
<form method="POST" action="/confirm/..." onsubmit="return confirm('...')">
    {% set text = 'Conferma e Invia' %}
    {% set icon = 'bi bi-check-circle' %}
    {% set variant = 'btn-success' %}
    {% set size = 'btn-lg w-100 h-100' %}
    {% set type = 'submit' %}
    {% include 'atoms/button.html' %}
</form>
```
---

### 🎯 Quando Usare Ciascuna Molecule

- **Stat Card**: KPI, metriche, contatori, dashboard statistics
- **Formazione Row**: Liste formazioni, tabelle dati, export reports
- **Flash Message**: Feedback utente, conferme operazioni, errori system
- **Preview Training Info**: Pagine conferma/preview dettagli formazione
- **Preview Telegram Messages**: Anteprima messaggi da inviare
- **Preview Email Section**: Anteprima email notifiche
- **Preview Action Form**: Riepilogo + conferma azioni critiche

---

## 🚀 Prossimi Passi

Ora che hai padroneggiato molecules e atoms, puoi procedere con:

1. **[Organisms](organisms.md)** - Sezioni complete (dashboard_stats, formazioni_table)
2. **[Templates/Pages](pages.md)** - Composizione finale (dashboard, login)
3. **[Layouts](layouts.md)** - Strutture di pagina (base, auth_required)

Le molecules sono il cuore del business logic - qui implementi le regole e i comportamenti specifici di Formazing! 🧬✨