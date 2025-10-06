# ⚛️ Atoms - Componenti Base

Gli **Atoms** sono i componenti più piccoli e riutilizzabili del sistema di design. Sono elementi HTML puri configurabili tramite props Jinja2, progettati per essere utilizzati in tutta l'applicazione mantenendo consistenza visiva e funzionale.

## 🎯 Filosofia degli Atoms

- **Riutilizzabili**: Un atom può essere usato ovunque nell'app
- **Configurabili**: Props permettono personalizzazione completa
- **Consistenti**: Stesso styling e comportamento in ogni contesto
- **Semplici**: Zero business logic, solo presentazione

---

## 🔘 Button - Bottone Universale

**File**: `templates/atoms/button.html`

### Descrizione
Bottone configurabile con supporto per icone, varianti di colore, dimensioni e eventi JavaScript.

### Props Disponibili
| Prop | Tipo | Default | Descrizione |
|------|------|---------|-------------|
| `text` | string | `'Button'` | Testo del bottone |
| `variant` | string | `'btn-primary'` | Classe Bootstrap per colore |
| `size` | string | `''` | Dimensione (`btn-sm`, `btn-lg`) |
| `icon` | string | - | Classe icona Bootstrap Icons |
| `type` | string | `'button'` | Tipo HTML (`button`, `submit`, `reset`) |
| `onclick` | string | - | Codice JavaScript da eseguire |
| `disabled` | boolean | `false` | Disabilita il bottone |
| `data_bs_toggle` | string | - | Attributo Bootstrap per modals/tabs |
| `data_bs_target` | string | - | Target Bootstrap per modals/tabs |

### Esempi di Utilizzo

#### Bottone Semplice
```html
{% include 'atoms/button.html' %}
{% set text = 'Salva' %}
```
**Risultato**: `<button class="btn btn-primary">Salva</button>`

#### Bottone con Icona
```html
{% include 'atoms/button.html' %}
{% set text = 'Elimina' %}
{% set icon = 'bi bi-trash' %}
{% set variant = 'btn-danger' %}
```
**Risultato**: `<button class="btn btn-danger"><i class="bi bi-trash"></i> Elimina</button>`

#### Bottone con Evento JavaScript
```html
{% set text = 'Aggiorna Dati' %}
{% set icon = 'bi bi-arrow-clockwise' %}
{% set variant = 'btn-outline-secondary' %}
{% set onclick = 'refreshData()' %}
{% include 'atoms/button.html' %}
```

#### Bottone per Navigazione (Link come Button)
```html
{% set text = 'Torna alla Dashboard' %}
{% set icon = 'bi bi-arrow-left' %}
{% set variant = 'btn-secondary' %}
{% set onclick = "window.location.href='" ~ url_for('main.dashboard') ~ "'" %}
{% include 'atoms/button.html' %}
```
**Nota**: Usando `onclick` con `window.location.href`, puoi creare button che navigano come link mantenendo lo stile consistente.

#### Bottone per Modal
```html
{% include 'atoms/button.html' %}
{% set text = 'Apri Modal' %}
{% set variant = 'btn-info' %}
{% set data_bs_toggle = 'modal' %}
{% set data_bs_target = '#myModal' %}
```

#### Bottone Disabilitato
```html
{% include 'atoms/button.html' %}
{% set text = 'Non Disponibile' %}
{% set variant = 'btn-secondary' %}
{% set disabled = true %}
```

### Varianti Colore Bootstrap
- `btn-primary` - Blu (default)
- `btn-secondary` - Grigio
- `btn-success` - Verde
- `btn-danger` - Rosso
- `btn-warning` - Giallo
- `btn-info` - Azzurro
- `btn-light` - Bianco
- `btn-dark` - Nero
- `btn-outline-*` - Versioni bordate

---

## 🏷️ Badge - Etichetta/Cartellino

**File**: `templates/atoms/badge.html`

### Descrizione
Piccola etichetta colorata per mostrare status, categorie o contatori. Supporta icone e colorazione automatica.

### Props Disponibili
| Prop | Tipo | Default | Descrizione |
|------|------|---------|-------------|
| `text` | string | `'Badge'` | Testo del badge |
| `color` | string | `'bg-secondary'` | Classe Bootstrap per colore sfondo |
| `icon` | string | - | Classe icona Bootstrap Icons |

### Esempi di Utilizzo

#### Badge Semplice
```html
{% include 'atoms/badge.html' %}
{% set text = 'Nuovo' %}
{% set color = 'bg-success' %}
```
**Risultato**: `<span class="badge bg-success">Nuovo</span>`

#### Badge con Icona
```html
{% include 'atoms/badge.html' %}
{% set text = 'IT' %}
{% set color = 'bg-info' %}
{% set icon = 'bi bi-laptop' %}
```
**Risultato**: `<span class="badge bg-info"><i class="bi bi-laptop"></i> IT</span>`

#### Badge Status Formazione
```html
<!-- Area formazione -->
{% include 'atoms/badge.html' %}
{% set text = formazione.get('Area', 'N/A') %}
{% set color = {
    'IT': 'bg-primary',
    'HR': 'bg-success',
    'Marketing': 'bg-warning'
}.get(formazione.get('Area'), 'bg-secondary') %}

<!-- Periodo formazione -->
{% include 'atoms/badge.html' %}
{% set text = formazione.get('Periodo', 'N/A') %}
{% set color = {
    'SPRING': 'bg-light text-dark',
    'AUTUMN': 'bg-warning',
    'ONCE': 'bg-info'
}.get(formazione.get('Periodo'), 'bg-secondary') %}
```

### Colori Bootstrap Disponibili
- `bg-primary` - Blu
- `bg-secondary` - Grigio  
- `bg-success` - Verde
- `bg-danger` - Rosso
- `bg-warning` - Giallo
- `bg-info` - Azzurro
- `bg-light text-dark` - Bianco con testo scuro
- `bg-dark` - Nero

---

## 📦 Card - Container Scatola

**File**: `templates/atoms/card.html`

### Descrizione
Container flessibile con header, body e footer opzionali. Base per tutti i contenuti strutturati.

### Props Disponibili
| Prop | Tipo | Default | Descrizione |
|------|------|---------|-------------|
| `content` | string | - | Contenuto HTML del body (richiesto) |
| `header` | string | - | Contenuto HTML dell'header |
| `footer` | string | - | Contenuto HTML del footer |
| `card_class` | string | `''` | Classi aggiuntive per la card |
| `header_class` | string | `''` | Classi per l'header |
| `body_class` | string | `''` | Classi per il body |
| `footer_class` | string | `''` | Classi per il footer |

### Esempi di Utilizzo

#### Card Semplice
```html
{% include 'atoms/card.html' %}
{% set content = '<h5>Titolo</h5><p>Contenuto della card</p>' %}
```

#### Card Completa
```html
{% include 'atoms/card.html' %}
{% set header = '<h6 class="mb-0">Statistiche Formazioni</h6>' %}
{% set content = '<h3 class="text-center">27</h3><p class="text-center mb-0">Totale</p>' %}
{% set footer = '<small class="text-muted">Ultimo aggiornamento: oggi</small>' %}
{% set card_class = 'border-primary' %}
```

#### Card Colorata
```html
{% include 'atoms/card.html' %}
{% set content = '<h3 class="text-center text-white">5</h3><p class="text-center text-white mb-0">Programmate</p>' %}
{% set card_class = 'bg-warning text-dark' %}
{% set body_class = 'text-center' %}
```

### Varianti Card Bootstrap
- `border-primary` - Bordo blu
- `bg-primary text-white` - Sfondo blu
- `shadow-sm` - Ombra leggera
- `shadow-lg` - Ombra pronunciata
- `border-0` - Nessun bordo

---

## 🖼️ Icon - Icona Universale

**File**: `templates/atoms/icon.html`

### Descrizione
Icona Bootstrap Icons configurabile per dimensione e colore.

### Props Disponibili
| Prop | Tipo | Default | Descrizione |
|------|------|---------|-------------|
| `name` | string | - | Nome icona Bootstrap Icons (richiesto) |
| `size` | string | `''` | Classe dimensione o spazio |
| `color` | string | `''` | Classe colore |

### Esempi di Utilizzo

#### Icona Semplice
```html
{% include 'atoms/icon.html' %}
{% set name = 'bi bi-house' %}
```
**Risultato**: `<i class="bi bi-house"></i>`

#### Icona Grande Colorata
```html
{% include 'atoms/icon.html' %}
{% set name = 'bi bi-speedometer2' %}
{% set size = 'display-4 mb-2' %}
{% set color = 'text-primary' %}
```

#### Icona con Margine
```html
{% include 'atoms/icon.html' %}
{% set name = 'bi bi-calendar-event' %}
{% set size = 'me-2' %}
```

#### Icone Comuni nell'App
```html
<!-- Dashboard -->
{% set name = 'bi bi-speedometer2' %}

<!-- Status formazioni -->
{% set name = 'bi bi-clock-history' %}    <!-- Programmata -->
{% set name = 'bi bi-calendar-event' %}   <!-- Calendarizzata -->
{% set name = 'bi bi-check-circle' %}     <!-- Conclusa -->

<!-- Azioni -->
{% set name = 'bi bi-eye' %}              <!-- Preview -->
{% set name = 'bi bi-download' %}         <!-- Export -->
{% set name = 'bi bi-gear' %}             <!-- Settings -->
{% set name = 'bi bi-plus' %}             <!-- Add -->
{% set name = 'bi bi-trash' %}            <!-- Delete -->
```

### Dimensioni Disponibili
- `display-1` a `display-6` - Molto grandi
- `fs-1` a `fs-6` - Font size standard
- `me-1`, `me-2`, etc. - Margine a destra
- `mb-1`, `mb-2`, etc. - Margine sotto

### Colori Disponibili
- `text-primary` - Blu
- `text-secondary` - Grigio
- `text-success` - Verde
- `text-danger` - Rosso
- `text-warning` - Giallo
- `text-info` - Azzurro
- `text-muted` - Grigio chiaro

---

## ⏳ Loading - Stati di Caricamento

**File**: `templates/atoms/loading.html`

### Descrizione
Spinner di caricamento configurabile con messaggio opzionale.

### Props Disponibili
| Prop | Tipo | Default | Descrizione |
|------|------|---------|-------------|
| `message` | string | - | Messaggio da mostrare accanto allo spinner |
| `size` | string | `''` | Dimensione spinner (`spinner-border-sm`) |
| `color` | string | `'text-primary'` | Colore spinner |
| `container_class` | string | `'p-4'` | Classi container |
| `text_class` | string | `'text-muted'` | Classi testo messaggio |

### Esempi di Utilizzo

#### Loading Semplice
```html
{% include 'atoms/loading.html' %}
```
**Risultato**: Spinner blu centrato con padding

#### Loading con Messaggio
```html
{% include 'atoms/loading.html' %}
{% set message = 'Caricamento formazioni...' %}
```

#### Loading Piccolo Inline
```html
{% include 'atoms/loading.html' %}
{% set size = 'spinner-border-sm' %}
{% set message = 'Salvando...' %}
{% set color = 'text-success' %}
{% set container_class = 'p-1' %}
```

#### Loading per Tabelle
```html
<tr>
    <td colspan="5">
        {% include 'atoms/loading.html' %}
        {% set message = 'Caricamento dati...' %}
        {% set container_class = 'py-4' %}
    </td>
</tr>
```
---

## 📱 Telegram Message Preview - Anteprima Messaggio Telegram

**File**: `templates/atoms/telegram_message_preview.html`

### Descrizione
Card specializzata per mostrare l'anteprima di un singolo messaggio Telegram con badge area e contenuto formattato. Utilizzato nelle pagine di preview notifiche.

### Props Disponibili
| Prop | Tipo | Default | Descrizione |
|------|------|---------|-------------|
| `area` | string | - | Nome dell'area destinataria (IT, HR, etc.) |
| `message_text` | string | - | Contenuto del messaggio da visualizzare |

### Caratteristiche
- **Badge automatico**: Usa internamente l'atomo badge con colore `bg-primary`
- **Formattazione testo**: `<pre>` con `white-space: pre-wrap` per preservare a capo
- **Scroll automatico**: Per messaggi lunghi (max-height: 400px)
- **Responsive**: Si adatta automaticamente al container

### Esempi di Utilizzo

#### Messaggio Singolo
```html
{% set area = 'IT' %}
{% set message_text = 'Ciao! Reminder formazione Python domani ore 15:00' %}
{% include 'atoms/telegram_message_preview.html' %}
```

#### In un Loop di Messaggi
```html
{% for message in telegram_messages %}
    {% set area = message.area %}
    {% set message_text = message.message %}
    {% include 'atoms/telegram_message_preview.html' %}
{% endfor %}
```

#### Messaggio con A Capo
```html
{% set area = 'HR' %}
{% set message_text = 'Formazione Leadership\nData: 15/10/2025\nOra: 14:30\n\nNon mancare!' %}
{% include 'atoms/telegram_message_preview.html' %}
```
**Risultato**: Gli a capo (`\n`) vengono preservati nel rendering grazie a `white-space: pre-wrap`

### Styling CSS
```css
/* Applicato automaticamente nel template */
pre {
    white-space: pre-wrap;      /* Preserva a capo */
    word-wrap: break-word;       /* Spezza parole lunghe */
    max-height: 400px;           /* Limite altezza */
    overflow: auto;              /* Scroll se necessario */
    font-size: 0.9rem;           /* Dimensione leggibile */
}
```
---

### 🎯 Quando Usare Ciascun Atom

- **Button**: Qualsiasi azione clickabile (submit, click, modal trigger, **navigazione**)
- **Badge**: Status, categorie, contatori, etichette
- **Card**: Raggruppare contenuti, stat displays, form sections
- **Icon**: Indicatori visuali, decorazioni, navigation hints
- **Loading**: Stati di caricamento, async operations, data fetching
- **Telegram Message Preview**: Anteprime messaggi Telegram nelle pagine di conferma/preview

---

## 🚀 Prossimi Passi

Una volta compresi gli atoms, puoi procedere con:

1. **[Molecules](molecules.md)** - Combinazioni di atoms (stat_card, formazione_row)
2. **[Organisms](organisms.md)** - Sezioni complete (dashboard_stats, formazioni_table)
3. **[Pages](pages.md)** - Composizione finale (dashboard, login)

Gli atoms sono i mattoni fondamentali - masterizzandoli avrai il controllo completo del design system! 🎨