# 🕸️ Dependency Graph - Sistema Template Formazing

Analisi completa delle dipendenze tra i componenti del sistema di template atomico.

---

## 🌐 Grafo Completo delle Dipendenze

```mermaid
graph TD
    %% Pages (Top Level)
    LP[📄 pages/login.html]:::page
    DP[📄 pages/dashboard.html]:::page
    
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
    
    %% Atoms
    BTN[⚛️ atoms/button.html]:::atom
    BDG[⚛️ atoms/badge.html]:::atom
    CRD[⚛️ atoms/card.html]:::atom
    ICN[⚛️ atoms/icon.html]:::atom
    LD[⚛️ atoms/loading.html]:::atom
    
    %% Page Dependencies
    LP --> BL
    DP --> AL
    AL --> BL
    
    %% Page to Organism Dependencies
    DP --> DS
    DP --> FT
    BL --> FM
    
    %% Organism to Molecule Dependencies
    DS --> SC
    FT --> FR
    FM --> FLM
    
    %% Molecule to Atom Dependencies
    SC --> ICN
    SC --> CRD
    FR --> BDG
    FR --> BTN
    FR --> ICN
    FLM --> ICN
    FLM --> BTN
    
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
    
    BTN[button.html]:::atom
    BDG[badge.html]:::atom
    CRD[card.html]:::atom
    ICN[icon.html]:::atom
    
    SC --> ICN
    SC --> CRD
    FR --> BDG
    FR --> BTN
    FR --> ICN
    FLM --> ICN
    FLM --> BTN
    
    classDef molecule fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef atom fill:#ffebee,stroke:#b71c1c,stroke-width:2px
```

**Dipendenze:**
- `stat_card.html` → `icon.html` + `card.html`
- `formazione_row.html` → `badge.html` + `button.html` + `icon.html`
- `flash_message.html` → `icon.html` + `button.html`

### ⚛️ Atoms (Livello 1)
```mermaid
graph LR
    BTN[button.html]:::atom
    BDG[badge.html]:::atom
    CRD[card.html]:::atom
    ICN[icon.html]:::atom
    LD[loading.html]:::atom
    
    classDef atom fill:#ffebee,stroke:#b71c1c,stroke-width:2px
```

**Tutti gli atoms sono componenti autonomi senza dipendenze interne.**

---

## 📈 Statistiche di Utilizzo

### Componenti più utilizzati (Incoming Dependencies)

| Componente | Utilizzato da | Frequenza |
|------------|---------------|-----------|
| `atoms/icon.html` | 3 molecules | 🔥🔥🔥 |
| `atoms/button.html` | 2 molecules | 🔥🔥 |
| `layout/base.html` | 2 layouts/pages | 🔥🔥 |
| `atoms/badge.html` | 1 molecule | 🔥 |
| `atoms/card.html` | 1 molecule | 🔥 |
| `atoms/loading.html` | 0 componenti | ⚠️ |

### Componenti più dipendenti (Outgoing Dependencies)

| Componente | Dipende da | Complessità |
|------------|------------|-------------|
| `molecules/formazione_row.html` | 3 atoms | 🔥🔥🔥 |
| `molecules/stat_card.html` | 2 atoms | 🔥🔥 |
| `molecules/flash_message.html` | 2 atoms | 🔥🔥 |
| `pages/dashboard.html` | 2 organisms | 🔥🔥 |

---


## 🔄 Impatti delle Modifiche

### Se modifichi un Atom
**Effetto a cascata verso l'alto:**

- `atoms/icon.html` → Impatta **3 molecules** + **4 organisms** + **2 pages**
- `atoms/button.html` → Impatta **2 molecules** + **3 organisms** + **2 pages**
- `atoms/card.html` → Impatta **1 molecule** + **1 organism** + **1 page**
- `atoms/badge.html` → Impatta **1 molecule** + **1 organism** + **1 page**
- `atoms/loading.html` → **Nessun impatto** (non utilizzato)

### Se modifichi una Molecule
**Effetto limitato:**

- `molecules/stat_card.html` → Impatta **1 organism** + **1 page**
- `molecules/formazione_row.html` → Impatta **1 organism** + **1 page**
- `molecules/flash_message.html` → Impatta **1 organism** + **2 pages**

### Se modifichi un Organism
**Effetto minimo:**

- Ogni organism impatta al massimo **1-2 pages**

---

## 🚨 Componenti a Rischio

### ⚠️ Atom Icon (Alto Rischio)
- **Utilizzato da:** 3 molecules
- **Impatto modifiche:** Molto alto
- **Raccomandazione:** Modifiche conservative, testing estensivo

### ⚠️ Layout Base (Alto Rischio)  
- **Utilizzato da:** Tutte le pages
- **Impatto modifiche:** Critico
- **Raccomandazione:** Solo modifiche essenziali

### ✅ Loading Atom (Rischio Zero)
- **Utilizzato da:** Nessuno
- **Stato:** Candidato per rimozione o integrazione futura

---


**Il grafo delle dipendenze ti aiuta a navigare e modificare il sistema in sicurezza!** 🎯✨