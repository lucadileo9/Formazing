# 🕸️ Dependency Graph - Sistema Template Formazing

Analisi completa delle dipendenze tra i componenti del sistema di template atomico.

---

## 🌐 Grafo Completo delle Dipendenze

```mermaid
graph TD
    %% Pages (Top Level)
    LP[📄 pages/login.html]:::page
    DP[📄 pages/dashboard.html]:::page
    PP[📄 pages/preview.html]:::page
    
    %% Layouts
    BL[🏗️ layout/base.html]:::layout
    AL[🏗️ layout/auth_required.html]:::layout
    
    %% Organisms
    DS[🦠 organisms/dashboard_stats.html]:::organism
    FT[🦠 organisms/formazioni_table.html]:::organism
    FM[🦠 organisms/flash_messages.html]:::organism
    TN[🦠 organisms/tab_navigation.html]:::organism
    
    %% Molecules
    SC[🧬 molecules/stat_card.html]:::molecule
    FR[🧬 molecules/formazione_row.html]:::molecule
    FLM[🧬 molecules/flash_message.html]:::molecule
    PTI[🧬 molecules/preview_training_info.html]:::molecule
    PTM[🧬 molecules/preview_telegram_messages.html]:::molecule
    PES[🧬 molecules/preview_email_section.html]:::molecule
    PAF[🧬 molecules/preview_action_form.html]:::molecule
    
    %% Atoms
    BTN[⚛️ atoms/button.html]:::atom
    BDG[⚛️ atoms/badge.html]:::atom
    CRD[⚛️ atoms/card.html]:::atom
    ICN[⚛️ atoms/icon.html]:::atom
    LD[⚛️ atoms/loading.html]:::atom
    TMP[⚛️ atoms/telegram_message_preview.html]:::atom
    
    %% Page Dependencies
    LP --> BL
    DP --> AL
    PP --> BL
    AL --> BL
    
    %% Page to Organism Dependencies
    DP --> DS
    DP --> FT
    BL --> FM
    
    %% Page to Molecule Dependencies (Preview page)
    PP --> PTI
    PP --> PTM
    PP --> PES
    PP --> PAF
    
    %% Organism to Molecule Dependencies
    DS --> SC
    FT --> FR
    FM --> FLM
    
    %% Molecule to Atom Dependencies (existing)
    SC --> ICN
    SC --> CRD
    FR --> BDG
    FR --> BTN
    FR --> ICN
    FLM --> ICN
    FLM --> BTN
    
    %% Molecule to Atom Dependencies (new preview molecules)
    PTI --> BDG
    PTM --> TMP
    PAF --> BDG
    PAF --> BTN
    
    %% Atom to Atom Dependencies
    TMP --> BDG
    
    %% Styling Classes
    classDef page fill:#e1f5fe,stroke:#01579b,stroke-width:3px,color:#000
    classDef layout fill:#f3e5f5,stroke:#4a148c,stroke-width:2px,color:#000
    classDef organism fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef molecule fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000
    classDef atom fill:#ffebee,stroke:#b71c1c,stroke-width:2px,color:#000
```

---

## 📊 Analisi per Livello

### 📄 Pages (Livello 5)
```mermaid
graph LR
    LP[login.html]:::page
    DP[dashboard.html]:::page
    
    BL[base.html]:::layout
    AL[auth_required.html]:::layout
    
    LP --> BL
    DP --> AL
    AL --> BL
    
    classDef page fill:#e1f5fe,stroke:#01579b,stroke-width:3px
    classDef layout fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
```

**Dipendenze:**
- `login.html` → `base.html` (direct)
- `dashboard.html` → `auth_required.html` → `base.html` (chain)
- `preview.html` → `base.html` (direct) + 4 preview molecules

### 🏗️ Layouts (Livello 4)
```mermaid
graph LR
    BL[base.html]:::layout
    AL[auth_required.html]:::layout
    FM[flash_messages.html]:::organism
    
    AL --> BL
    BL --> FM
    
    classDef layout fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef organism fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
```

**Dipendenze:**
- `auth_required.html` → `base.html` (inheritance)
- `base.html` → `flash_messages.html` (include)

### 🦠 Organisms (Livello 3)
```mermaid
graph TD
    DS[dashboard_stats.html]:::organism
    FT[formazioni_table.html]:::organism
    FM[flash_messages.html]:::organism
    TN[tab_navigation.html]:::organism
    
    SC[stat_card.html]:::molecule
    FR[formazione_row.html]:::molecule
    FLM[flash_message.html]:::molecule
    
    DS --> SC
    FT --> FR
    FM --> FLM
    
    classDef organism fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef molecule fill:#fff3e0,stroke:#e65100,stroke-width:2px
```

**Dipendenze:**
- `dashboard_stats.html` → `stat_card.html`
- `formazioni_table.html` → `formazione_row.html`
- `flash_messages.html` → `flash_message.html`
- `tab_navigation.html` → standalone (usa solo Bootstrap)

### 🧬 Molecules (Livello 2)
```mermaid
graph TD
    SC[stat_card.html]:::molecule
    FR[formazione_row.html]:::molecule
    FLM[flash_message.html]:::molecule
    PTI[preview_training_info.html]:::molecule
    PTM[preview_telegram_messages.html]:::molecule
    PES[preview_email_section.html]:::molecule
    PAF[preview_action_form.html]:::molecule
    
    BTN[button.html]:::atom
    BDG[badge.html]:::atom
    CRD[card.html]:::atom
    ICN[icon.html]:::atom
    TMP[telegram_message_preview.html]:::atom
    
    SC --> ICN
    SC --> CRD
    FR --> BDG
    FR --> BTN
    FR --> ICN
    FLM --> ICN
    FLM --> BTN
    PTI --> BDG
    PTM --> TMP
    PAF --> BDG
    PAF --> BTN
    TMP --> BDG
    
    classDef molecule fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef atom fill:#ffebee,stroke:#b71c1c,stroke-width:2px
```

**Dipendenze:**
- `stat_card.html` → `icon.html` + `card.html`
- `formazione_row.html` → `badge.html` + `button.html` + `icon.html`
- `flash_message.html` → `icon.html` + `button.html`
- `preview_training_info.html` → `badge.html` (per Area e Stato)
- `preview_telegram_messages.html` → `telegram_message_preview.html`
- `preview_email_section.html` → standalone (nessuna dipendenza atom)
- `preview_action_form.html` → `badge.html` + `button.html`

### ⚛️ Atoms (Livello 1)
```mermaid
graph LR
    BTN[button.html]:::atom
    BDG[badge.html]:::atom
    CRD[card.html]:::atom
    ICN[icon.html]:::atom
    LD[loading.html]:::atom
    TMP[telegram_message_preview.html]:::atom
    
    TMP --> BDG
    
    classDef atom fill:#ffebee,stroke:#b71c1c,stroke-width:2px
```

**Quasi tutti gli atoms sono componenti autonomi, tranne:**
- `telegram_message_preview.html` → dipende da `badge.html`

---

## 📈 Statistiche di Utilizzo

### Componenti più utilizzati (Incoming Dependencies)

| Componente | Utilizzato da | Frequenza |
|------------|---------------|-----------|
| `atoms/badge.html` | 4 molecules | 🔥🔥🔥🔥 |
| `atoms/button.html` | 3 molecules | 🔥🔥🔥 |
| `atoms/icon.html` | 3 molecules | 🔥🔥🔥 |
| `layout/base.html` | 3 pages | 🔥🔥🔥 |
| `atoms/card.html` | 1 molecule | 🔥 |
| `atoms/telegram_message_preview.html` | 1 molecule | 🔥 |
| `atoms/loading.html` | 0 componenti | ⚠️ |

### Componenti più dipendenti (Outgoing Dependencies)

| Componente | Dipende da | Complessità |
|------------|------------|-------------|
| `molecules/formazione_row.html` | 3 atoms | 🔥🔥🔥 |
| `pages/preview.html` | 4 molecules | 🔥🔥🔥🔥 |
| `molecules/preview_action_form.html` | 2 atoms | 🔥🔥 |
| `molecules/stat_card.html` | 2 atoms | 🔥🔥 |
| `molecules/flash_message.html` | 2 atoms | 🔥🔥 |
| `molecules/preview_training_info.html` | 1 atom | 🔥 |
| `molecules/preview_telegram_messages.html` | 1 atom | 🔥 |

---


## 🔄 Impatti delle Modifiche

### Se modifichi un Atom
**Effetto a cascata verso l'alto:**

- `atoms/badge.html` → Impatta **5 componenti** (4 molecules + telegram_message_preview) + **2 pages**
- `atoms/button.html` → Impatta **3 molecules** + **3 organisms** + **2 pages**
- `atoms/icon.html` → Impatta **3 molecules** + **4 organisms** + **2 pages**
- `atoms/telegram_message_preview.html` → Impatta **1 molecule** + **1 page**
- `atoms/card.html` → Impatta **1 molecule** + **1 organism** + **1 page**
- `atoms/loading.html` → **Nessun impatto** (non utilizzato)

### Se modifichi una Molecule
**Effetto limitato:**

- `molecules/stat_card.html` → Impatta **1 organism** + **1 page**
- `molecules/formazione_row.html` → Impatta **1 organism** + **1 page**
- `molecules/flash_message.html` → Impatta **1 organism** + **2 pages**
- `molecules/preview_training_info.html` → Impatta **1 page** (preview)
- `molecules/preview_telegram_messages.html` → Impatta **1 page** (preview)
- `molecules/preview_email_section.html` → Impatta **1 page** (preview)
- `molecules/preview_action_form.html` → Impatta **1 page** (preview)

### Se modifichi un Organism
**Effetto minimo:**

- Ogni organism impatta al massimo **1-2 pages**

---

## 🚨 Componenti a Rischio

### ⚠️ Atom Badge (Alto Rischio) - **NUOVO LEADER**
- **Utilizzato da:** 4 molecules + 1 atom
- **Impatto modifiche:** Molto alto
- **Raccomandazione:** Modifiche conservative, testing estensivo su tutte le preview

### ⚠️ Atom Icon (Alto Rischio)
- **Utilizzato da:** 3 molecules
- **Impatto modifiche:** Alto
- **Raccomandazione:** Modifiche conservative, testing estensivo

### ⚠️ Atom Button (Alto Rischio)
- **Utilizzato da:** 3 molecules
- **Impatto modifiche:** Alto
- **Raccomandazione:** Testing su formazione_row, flash_message e preview_action_form

### ⚠️ Layout Base (Alto Rischio)  
- **Utilizzato da:** Tutte le 3 pages
- **Impatto modifiche:** Critico
- **Raccomandazione:** Solo modifiche essenziali

### ⚠️ Preview Page (Dipendenze Multiple)
- **Dipende da:** 4 molecules preview
- **Complessità:** Alta
- **Raccomandazione:** Testing completo user flow notifiche/feedback

### ✅ Loading Atom (Rischio Zero)
- **Utilizzato da:** Nessuno
- **Stato:** Candidato per rimozione o integrazione futura

---


**Il grafo delle dipendenze ti aiuta a navigare e modificare il sistema in sicurezza!** 🎯✨