# 🚀 Guida Completa ad Agile & Scrum

**Metodologie agili per team ad alte prestazioni**

---

## 📚 Indice

1. [Manifesto Agile](#1-manifesto-agile)
2. [Principi Agile](#2-principi-agile)
3. [Scrum Framework](#3-scrum-framework)
4. [Sprint Planning](#4-sprint-planning)
5. [Daily Scrum](#5-daily-scrum)
6. [Sprint Review & Retrospective](#6-sprint-review--retrospective)
7. [Product Backlog](#7-product-backlog)
8. [User Stories](#8-user-stories)
9. [Estimation & Velocity](#9-estimation--velocity)
10. [Metriche Agile](#10-metriche-agile)
11. [Scaling Agile](#11-scaling-agile)
12. [Common Pitfalls](#12-common-pitfalls)

---

## 1. Manifesto Agile

### 1.1 I 4 Valori

```
Individui e Interazioni    >    Processi e Strumenti
Software Funzionante       >    Documentazione Esaustiva
Collaborazione Cliente     >    Negoziazione Contratti
Risposta al Cambiamento   >    Seguire un Piano
```

**Non significa:**
- ❌ Zero processi
- ❌ Zero documentazione
- ❌ Zero contratti
- ❌ Zero pianificazione

**Significa:**
- ✅ Valorizziamo di PIÙ ciò a sinistra
- ✅ Bilanciamo in base al contesto
- ✅ Pragmatismo over dogma

### 1.2 Quando Agile?

**✅ Usa Agile quando:**
- Requisiti non completamente chiari all'inizio
- Prodotto complesso, innovativo
- Mercato in rapida evoluzione
- Feedback frequente è critico
- Team collocato (o ben coordinato remote)
- Stakeholder disponibili e coinvolti

**❌ Evita Agile quando:**
- Requisiti fissi, ben definiti, stabili
- Progetti con compliance rigida (es. costruzioni, hardware)
- Team non dedicato o part-time
- Stakeholder non disponibili
- Contratti fixed-price/fixed-scope rigidi

---

## 2. Principi Agile

**I 12 Principi dietro il Manifesto:**

1. **Soddisfazione cliente** attraverso consegna continua di software di valore
2. **Benvenuti cambiamenti** anche tardi nello sviluppo
3. **Consegna frequente** di software funzionante (settimane, non mesi)
4. **Business e dev lavorano insieme** quotidianamente
5. **Motiva individui** - Dai fiducia e supporto
6. **Face-to-face** è il metodo migliore di comunicazione
7. **Software funzionante** è la misura principale di progresso
8. **Ritmo sostenibile** - No burn out
9. **Eccellenza tecnica** e buon design potenziano agilità
10. **Semplicità** - Massimizza il lavoro non fatto
11. **Team auto-organizzati** producono le migliori soluzioni
12. **Reflect & adjust** regolarmente

---

## 3. Scrum Framework

### 3.1 Pilastri di Scrum

**1. Trasparenza**
- Processo visibile a tutti
- Definizioni condivise
- Artefatti accessibili

**2. Ispezione**
- Controllo frequente artefatti e progresso
- Detect variations early

**3. Adattamento**
- Aggiusta processo se fuori accettabile
- Quick corrections

### 3.2 Ruoli Scrum

#### **Product Owner (PO)**

**Responsabilità:**
- ✅ Massimizza valore del prodotto
- ✅ Gestisce e prioritizza Product Backlog
- ✅ Definisce acceptance criteria
- ✅ Decide cosa va in ogni Sprint
- ✅ È voce unica del cliente

**Non fa:**
- ❌ Gestione team (non è project manager)
- ❌ Assegna task ai membri
- ❌ Micromanage implementazione

**Skills chiave:**
- Vision del prodotto
- Business acumen
- Decision making
- Stakeholder management
- Comunicazione

#### **Scrum Master (SM)**

**Responsabilità:**
- ✅ Facilita eventi Scrum
- ✅ Rimuove impedimenti
- ✅ Coach team su Scrum
- ✅ Protegge team da distrazioni
- ✅ Promuove auto-organizzazione

**Non fa:**
- ❌ Project manager tradizionale
- ❌ Boss del team
- ❌ Assegna lavoro

**Skills chiave:**
- Facilitation
- Coaching
- Conflict resolution
- Servant leadership
- Change management

#### **Development Team**

**Caratteristiche:**
- 👥 **Size:** 3-9 persone (ideale 5-7)
- 🎯 **Cross-functional:** Tutte skill necessarie
- 🔄 **Self-organizing:** Decidono come lavorare
- 🏆 **Accountable:** Responsabili collettivamente
- 🚫 **No titoli:** Tutti sono "Developer"
- 🚫 **No sub-team:** Uno solo team

**Responsabilità:**
- ✅ Consegna Increment ogni Sprint
- ✅ Auto-gestione task
- ✅ Qualità del prodotto
- ✅ Stima effort

### 3.3 Eventi Scrum (Cerimonie)

```
Sprint (2-4 settimane)
├── Sprint Planning (4h per 2-week sprint)
├── Daily Scrum (15 min × giorni)
├── Sprint Review (2h per 2-week sprint)
└── Sprint Retrospective (1.5h per 2-week sprint)
```

**Timeboxing rigoroso!**

---

## 4. Sprint Planning

**Durata:** Max 8h per sprint 1 mese (4h per 2 settimane)

**Partecipanti:** PO, SM, Dev Team

### 4.1 Parte 1: COSA faremo?

**Input:**
- Product Backlog (prioritizzato)
- Latest Increment
- Capacity team per sprint
- Definition of Done

**PO presenta:**
- Obiettivo Sprint (Sprint Goal)
- Top priority items dal Backlog

**Team discute:**
- Comprensione dei requisiti
- Fa domande al PO
- Stima complexity

**Output:**
- **Sprint Goal** - Obiettivo coerente
- **Sprint Backlog** - PBI selezionati

**Sprint Goal esempio:**
```
"Permettere agli utenti di registrarsi e fare login,
così possono salvare i loro dati per visite future"
```

### 4.2 Parte 2: COME lo faremo?

**Team decompone PBI in task:**

User Story: "Come utente, voglio registrarmi"

Task breakdown:
- [ ] Design form registrazione
- [ ] Implementa frontend form
- [ ] Create API endpoint registrazione
- [ ] Setup database user table
- [ ] Hashing password
- [ ] Email verification flow
- [ ] Unit tests
- [ ] Integration tests
- [ ] UI validation errors
- [ ] Accessibility check

**Stima task in ore:** (opzionale, alcuni team usano solo story points)

**Output finale Sprint Planning:**
- Sprint Goal
- Sprint Backlog (PBI + task)
- Piano di massima per consegna

---

## 5. Daily Scrum

**Durata:** Max 15 minuti
**Quando:** Stessa ora ogni giorno
**Dove:** Stesso posto (o Zoom)
**Partecipanti:** Dev Team (required), SM facilita, PO può assistere

### 5.1 Formato Classico (3 Domande)

Ogni membro condivide:
1. **Cosa ho fatto ieri** che ha aiutato il team verso lo Sprint Goal?
2. **Cosa farò oggi** per aiutare il team verso lo Sprint Goal?
3. **Vedo qualche impedimento** che blocca me o il team?

**Esempio:**
```
Alice: "Ieri ho completato l'API di registrazione.
       Oggi integrerò il frontend con l'API.
       Nessun blocco."

Bob:   "Ieri ho lavorato sui tests, 80% fatto.
       Oggi finisco tests e inizio email verification.
       Blocco: non ho accesso al server email di staging."

SM:    "Ok Bob, risolvo accesso server entro oggi pomeriggio"
```

### 5.2 Formati Alternativi

**Walk the Board:**
Invece di per persona, vai per task.
```
"Questo task è in progress, chi ci sta lavorando?"
"Questo task è bloccato, come lo risolviamo?"
```

**Focus su Sprint Goal:**
```
"Cosa ci avvicina allo Sprint Goal oggi?"
"Cosa ci sta rallentando?"
```

### 5.3 Best Practices

✅ **Do:**
- Stessa ora ogni giorno
- Stare in piedi (mantiene breve)
- Focalizzati su Sprint Goal
- Risolvi impedimenti subito
- Aggiorna board in tempo reale

❌ **Don't:**
- > 15 minuti
- Problem solving (parking lot)
- Status report al manager
- Dettagli tecnici lunghi
- Presenze non necessarie

---

## 6. Sprint Review & Retrospective

### 6.1 Sprint Review

**Scopo:** Inspect & adapt il PRODOTTO

**Durata:** Max 4h per sprint 1 mese (2h per 2 settimane)

**Partecipanti:** Team, PO, Stakeholder, chiunque interessato

**Agenda:**
1. **PO riepiloga Sprint Goal** e cosa era pianificato
2. **Team demo** l'Increment funzionante
   - Solo roba DONE (secondo DoD)
   - Live demo, no slide
3. **PO review Product Backlog:**
   - Cosa è Done
   - Cosa non è Done (torna in Backlog)
   - Proiezione date basate su progresso
4. **Feedback stakeholder**
5. **Discussione cosa fare next**
6. **Review timeline, budget, marketplace**

**Output:**
- Product Backlog aggiornato
- Probabili PBI per prossimo Sprint

**Tips:**
- 📺 Demo reale, working software
- 🎯 Focus su valore business
- 💬 Incoraggia feedback onesto
- 📝 Cattura feedback per Backlog refinement

### 6.2 Sprint Retrospective

**Scopo:** Inspect & adapt il PROCESSO

**Durata:** Max 3h per sprint 1 mese (1.5h per 2 settimane)

**Partecipanti:** Dev Team, SM, PO (opzionale)

**Domande chiave:**
1. **Cosa è andato BENE?** (Keep doing)
2. **Cosa è andato MALE?** (Stop doing)
3. **Cosa possiamo MIGLIORARE?** (Start doing)

**Format esempio: Start/Stop/Continue**

```
┌─────────────┬──────────────┬────────────────┐
│ START       │ STOP         │ CONTINUE       │
├─────────────┼──────────────┼────────────────┤
│ • Code      │ • Meetings   │ • Pair         │
│   reviews   │   senza      │   programming  │
│   su tutti  │   agenda     │                │
│   PR        │              │ • Daily        │
│             │ • Push su    │   standups     │
│ • Automated │   master     │                │
│   tests in  │   senza PR   │                │
│   CI/CD     │              │                │
└─────────────┴──────────────┴────────────────┘
```

**Tecniche Facilitazione:**

**1. Mad/Sad/Glad**
```
😠 Mad:    Cosa ci ha frustrato?
😢 Sad:    Cosa ci ha deluso?
😊 Glad:   Cosa ci ha reso felici?
```

**2. Sailboat/Speedboat**
```
⛵ Vento (accelera):    Cosa ci aiuta?
⚓ Ancora (rallenta):   Cosa ci frena?
🪨 Rocce (rischi):     Cosa temiamo?
```

**3. Timeline Retrospective**
Disegna timeline sprint, segna eventi chiave, discuti.

**Output:**
- Lista di miglioramenti da implementare
- **Action items** con owner e deadline
- Update "Definition of Done" se necessario

**Regola d'oro:**
> "Assume everyone did their best with
> knowledge, skills, and resources available"

---

## 7. Product Backlog

### 7.1 Struttura Backlog

**Formato tipico:**
```
High Priority (Sprint-ready)
├── User Story 1  [13 pts] - Ready
├── User Story 2  [8 pts]  - Ready
├── User Story 3  [5 pts]  - Ready
│
Medium Priority (Being refined)
├── User Story 4  [21 pts] - Needs breakdown
├── User Story 5  [?]      - Needs estimation
│
Low Priority (Future)
├── Epic 1 - "Mobile App"
├── Epic 2 - "Admin Dashboard"
│
Icebox (Maybe someday)
└── Nice-to-have ideas
```

### 7.2 Grooming/Refinement

**Attività continua (non evento ufficiale Scrum):**
- ~10% time del team
- Mid-sprint spesso
- PO + alcuni dev

**Attività:**
1. **Dettagliare** PBI top priority
2. **Stimare** nuovi item
3. **Decompositi** Epics in User Stories
4. **Riordinare** priorità
5. **Rimuovere** item obsoleti

**Goal:**
Top ~2 Sprint worth di lavoro sono "Ready"

**Definition of Ready (DoR):**
```
✅ Chiaro e comprensibile
✅ Testabile
✅ Stimato
✅ Acceptance criteria definiti
✅ Dipendenze identificate
✅ Small enough (fit in 1 sprint)
```

---

## 8. User Stories

### 8.1 Formato Standard

```
Come [tipo utente]
Voglio [azione/funzionalità]
Così che [beneficio/valore]
```

**Esempi:**

❌ "Implementa login"
✅ "Come utente registrato, voglio fare login con email e password,
   così che possa accedere al mio account salvato"

❌ "Aggiungi ricerca"
✅ "Come cliente, voglio cercare prodotti per nome o categoria,
   così che possa trovare rapidamente quello che mi serve"

### 8.2 Acceptance Criteria

**Dato/Quando/Allora (Given/When/Then):**

```
User Story: Login

AC1: Login con credenziali valide
  Dato che sono sulla pagina login
  Quando inserisco email e password corrette
  Allora vengo portato alla dashboard

AC2: Login con password sbagliata
  Dato che sono sulla pagina login
  Quando inserisco password errata
  Allora vedo messaggio "Credenziali invalide"
  E rimango sulla pagina login

AC3: Login con account non esistente
  Dato che sono sulla pagina login
  Quando inserisco email non registrata
  Allora vedo messaggio "Account non trovato"

AC4: Validazione form
  Dato che sono sulla pagina login
  Quando lascio email vuota
  Allora vedo errore "Email richiesta"
```

**Checklist style:**
```
✅ Login con credenziali valide porta a dashboard
✅ Password errata mostra messaggio errore
✅ Email non esistente mostra messaggio errore
✅ Validazione client-side sui campi
✅ Password deve essere nascosta (****)
✅ Link "Password dimenticata" funziona
✅ Accessibile da tastiera (tab navigation)
✅ Responsive (mobile + desktop)
```

### 8.3 INVEST Criteria

User Story di qualità sono:

- **I**ndependent - Può essere sviluppata da sola
- **N**egotiable - Dettagli flessibili
- **V**aluable - Valore per utente/business
- **E**stimable - Team può stimare
- **S**mall - Fit in uno sprint
- **T**estable - Criteri accettazione chiari

---

## 9. Estimation & Velocity

### 9.1 Story Points

**Cosa sono:**
Misura relativa di effort/complexity/uncertainty.

**Non sono:**
- ❌ Ore
- ❌ Giorni
- ❌ Productivity metric individuale

**Scala Fibonacci:**
```
1, 2, 3, 5, 8, 13, 21, 34, 55, 89...
```

**Perché Fibonacci?**
Riflette incertezza crescente per item grandi.

**Reference Stories:**
```
1 pt:  Typo fix in UI
2 pts: Aggiungi campo a form esistente
3 pts: Nuovo semplice form
5 pts: Feature con API + UI
8 pts: Feature complessa multi-page
13 pts: Troppo grande, break down!
```

### 9.2 Planning Poker

**Processo:**
1. PO presenta User Story
2. Team fa domande
3. Ciascuno sceglie card (1,2,3,5,8,13...) segretamente
4. Tutti rivelano simultaneamente
5. **Se consensus** → stima decisa
6. **Se divergenza** → Highest e lowest spiegano rationale
7. Ripeti 4-6 finché consensus

**Tools:**
- Card fisiche
- App: PlanningPoker.com, ScrumPoker online

### 9.3 Velocity

**Velocity = Story Points completati per Sprint**

**Esempio:**
```
Sprint 1:  18 pts
Sprint 2:  22 pts
Sprint 3:  20 pts
Sprint 4:  19 pts
-----------------------
Average Velocity: 19.75 pts/sprint
```

**Uso:**
- **Planning:** "Abbiamo capacity ~20 pts"
- **Forecasting:** "100 pts backlog / 20 = 5 sprint (~10 weeks)"

**⚠️ NON usare Velocity per:**
- ❌ Comparare team diversi
- ❌ Performance review individuali
- ❌ Incentivi/bonus
- ❌ Pressure per aumentare

---

## 10. Metriche Agile

### 10.1 Burndown Chart

**Sprint Burndown:**
```
Story Points Remaining
│
30│ \
  │  \  Ideal
25│   \____
  │    \   Actual
20│     ----\__
  │           \___
15│               --\
  │                  \
10│                   \
  │                    ---
 5│                       ----___
  │                              ----___
 0└──────────────────────────────────────
  Day 1  3   5   7   9   11  13  15
```

**Interpretazione:**
- **Sopra ideal:** Ritardo
- **Sotto ideal:** Ahead
- **Piatto:** Nessun progress (problemi!)

### 10.2 Burnup Chart

```
Points
│                            /------- Total Scope
│                          /
│                        /
│                      /
30│                   /
  │               / /
25│            /  /
  │         /   /
20│      /    /─────── Completed Work
  │   /     /
15│ /      /
  │/      /
10│      /
  │     /
 5│    /
  │   /
 0└───────────────
  Sprint 1 2 3 4 5
```

**Meglio di Burndown perché:**
- Mostra scope changes
- Trend completamento visibile
- Forecast più chiaro

### 10.3 Cumulative Flow Diagram (CFD)

```
Tasks
│        ┌─────────── Done
│      ┌─┴────────── Review
│    ┌─┴──────────── In Progress
│  ┌─┴────────────── To Do
│┌─┴──────────────── Backlog
└─────────────────────────────── Time
```

**Identifica:**
- **Bottleneck** - Colonna che si allarga
- **WIP troppo alto** - Area "In Progress" grossa
- **Throughput** - Velocità crescita "Done"

### 10.4 Lead Time & Cycle Time

**Lead Time:**
Ticket created → Delivered
(Prospettiva cliente)

**Cycle Time:**
Work started → Delivered
(Prospettiva team)

**Target:**
- Minimize both
- Consistent (predictable)

---

## 11. Scaling Agile

### 11.1 SAFe (Scaled Agile Framework)

**4 livelli:**
```
Portfolio (Strategy)
    ↓
Large Solution (Coordination)
    ↓
Program (multiple teams)
    ↓
Team (Scrum base)
```

**Introduce:**
- PI (Program Increment) - 8-12 week planning cycle
- ART (Agile Release Train) - Team di team
- Scrum of Scrums - Sync multi-team

### 11.2 Scrum@Scale

**Team di Team:**
```
Scrum of Scrums
    - Rep da ogni team
    - Daily sync
    - Risolve dependencies

Executive Action Team
    - Leadership
    - Resource allocation
```

### 11.3 Nexus (Scrum.org)

**3-9 Scrum Teams** su stesso prodotto
- Shared Product Backlog
- Nexus Integration Team coordina
- Nexus Sprint Review combinata

---

## 12. Common Pitfalls

### 12.1 Anti-Patterns

**1. Scrum-but**
"Facciamo Scrum, MA..."
- ...no Daily Standup
- ...no Retrospectives
- ...Sprint di 6 settimane
→ **Fix:** Segui framework correttamente prima di adattare

**2. Story Points = Hours**
"1 pt = 1 hour"
→ **Fix:** Points sono relativi, non assoluti

**3. Velocity Pressure**
"Dobbiamo aumentare velocity!"
→ **Fix:** Velocity è forecasting tool, non target

**4. No Definition of Done**
"È quasi finito... manca solo..."
→ **Fix:** DoD chiaro e applicato rigidamente

**5. PO Assente**
PO non disponibile durante Sprint
→ **Fix:** PO committed full-time (o almeno disponibile)

**6. Technical Debt Ignorato**
"Facciamo solo feature, refactoring dopo"
→ **Fix:** 10-20% Sprint capacity per tech debt

**7. Retrospective Superficiale**
"Tutto ok, continuiamo così"
→ **Fix:** Facilitation vera, psychological safety

### 12.2 Transizione da Waterfall

**Sfide comuni:**

**Culturale:**
- Command-control → Servant leadership
- Plan rigido → Adaptive planning
- Silos → Cross-functional teams

**Organizzativo:**
- Fixed teams → Stable dedicated teams
- Resource pool → Product teams
- Annual planning → Incremental planning

**Tecnico:**
- Manual testing → Automated testing
- Infrequent releases → Continuous delivery
- Long branches → Trunk-based development

**Strategia transizione:**
1. **Pilot team** - Prova con 1 team
2. **Coach & train** - Invest in learning
3. **Adapt org** - Remove impediments
4. **Scale gradualmente**
5. **Patience** - 6-12 mesi per maturare

---

## 🎯 Riassunto Checklist

### Sprint 0 (Setup)
- [ ] Team formato (5-7 persone cross-functional)
- [ ] Ruoli assegnati (PO, SM)
- [ ] Product vision chiara
- [ ] Initial Product Backlog (top 2-3 sprint worth)
- [ ] Definition of Done concordata
- [ ] Tools setup (Jira, board)

### Ogni Sprint
- [ ] Sprint Planning (Sprint Goal + Sprint Backlog)
- [ ] Daily Scrum (15 min, ogni giorno)
- [ ] Development work (self-organized)
- [ ] Sprint Review (demo + feedback)
- [ ] Sprint Retrospective (improve process)

### Continuous
- [ ] Backlog refinement (~10% time)
- [ ] Track impediments
- [ ] Update board daily
- [ ] Monitor metrics (velocity, burndown)

---

**Agile è mindset, non solo processo. Abbraccia cambiamento! 🚀**
