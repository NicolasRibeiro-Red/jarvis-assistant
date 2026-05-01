# /tasks — Task Management + Kanban Dashboard

**Triggers**: `/tasks`, `tarefas`, `task`, `kanban`, `dashboard`, `adicionar tarefa`, `listar tarefas`, `o que tenho pra fazer`

**Purpose**: Manage the principal's tasks across the lifecycle — capture, prioritize, move through pipeline, complete, archive. Default view is a **terminal-native Kanban** inspired by the Geist Design System (monochrome-first, hairline borders, high density, no decoration).

---

## Data model

Each task is a markdown file at `memory/tasks/T-{YYYY-MM-DD}-{seq}.md`:

```yaml
---
id: T-2026-05-01-1
title: "Apresentacao quinta-feira"
column: hoje              # backlog | hoje | doing | done
priority: high            # high | medium | low
project: "Cliente X"      # optional, groups in kanban
due: 2026-05-08           # optional, ISO date
created: 2026-05-01
completed: null           # ISO date when column = done
---
[Free-form description body if useful — most tasks need none]
```

**Column = pipeline state. Priority = importance.** They are independent.

| Column | Meaning |
|--------|---------|
| `backlog` | Captured, not yet committed to any day |
| `hoje` | Committed to today (or imminent — next 24-48h) |
| `doing` | Active work right now (max 3 — WIP limit) |
| `done` | Completed (auto-archives 14 days after `completed`) |

Legacy compatibility: tasks created with `status: pending|in-progress|done` (v1.6 schema) are auto-mapped on read:
- `pending` → `backlog` if no due, `hoje` if due ≤ tomorrow
- `in-progress` → `doing`
- `done` → `done`

---

## Operations

### ADD — capture a new task
**Triggers**: principal mentions a deadline, says *"preciso fazer X"*, *"adiciona X"*, *"tenho que..."*

Workflow:
1. Extract: title, priority (infer from urgency cues; ask only if genuinely ambiguous), due date if mentioned, project if mentioned
2. Decide column:
   - Has due ≤ today → `hoje`
   - Has due ≤ tomorrow → `hoje`
   - Has due in future → `backlog`
   - No due, urgent language → `hoje`
   - No due, no urgency → `backlog`
3. Generate ID: `T-{YYYY-MM-DD}-{seq}` (seq = number of tasks created today)
4. Write file. Confirm in CLINICAL register, voice-matched:
   *"Registrado. '[title]' — [column], prioridade [priority][, prazo DD/MM]."*

**Never ask the principal what column to use unless the task is truly ambiguous.** Default to backlog if uncertain.

**Anti-duplicate check**: before writing, search existing tasks by title fuzzy match (Levenshtein ≤ 30%). If close match exists, surface it: *"Tarefa similar ja existe: '[existing]'. Deseja substituir, atualizar prazo, ou criar mesmo assim?"*

### LIST — show the Kanban (default view)

**Triggers**: `tarefas`, `kanban`, `dashboard`, `listar`, `o que tenho pra fazer`

Workflow:
1. Read all files in `memory/tasks/` (skip `done/` archive)
2. Classify by column. Within each column, sort by priority (high → medium → low), then by due date (earliest first)
3. Compute counts per column
4. Render Kanban (see format below)
5. Run humanize-check
6. Deliver

**Render format** (Geist terminal-native — monochrome, hairline, high-density):

```
J.A.R.V.I.S.  Tarefas                                    [Dia], DD/MM

▌ HOJE  ──────────────────────────────────────────────────  [N] itens
○ [task title shortened to ~40 chars]              alta    DD/MM
○ [task title]                                     media   hoje
○ [task title]                                     baixa   hoje

◐ DOING  ─────────────────────────────────────────────────  [N] itens
◐ [task title]                                     alta    em ~%
◐ [task title]                                     media   em ~%

○ BACKLOG  ───────────────────────────────────────────────  [N] itens
○ [task title]                                     media   sem prazo
○ [task title]                                     baixa   DD/MM
○ [task title]                                     baixa   sem prazo
+ [N] outras

● DONE (esta semana)  ────────────────────────────────────  [N] itens
● [task title]                                     DD/MM
● [task title]                                     DD/MM
+ [N] outras

[total] tarefas  ·  [N] vencidas  ·  taxa de conclusao: [%] (7 dias)

[Recommendation — 1 sentence, register-appropriate, voice-matched.
 Connect to deadline, objective, or confirmed pattern.]

1. [primary action — usually start the recommended task]
2. [secondary — move/update]
3. Adicionar tarefa
4. Outra coisa
```

**Visual rules**:
- Symbols: `○` pending (backlog/hoje), `◐` doing (in progress), `●` done, `▌` accent (urgent/today section)
- Separators: only `─` (hairline). Never `═` `╔` `╗` etc — those are AI-pattern overhead
- No emoji, no spark lines, no progress bars, no gauges
- Column headers: `▌ NAME  ──...──  [N] itens` — single line, accent bar prefix
- Density: tasks aligned in 3 columns (title | priority | deadline), monospace handles alignment
- Truncate title at 40 chars + ellipsis. Truncate column to 8 visible items, summarize rest as `+ [N] outras`
- Spacing: 1 blank line between sections (the 24px gap rhythm)

**Empty columns**: if `hoje` has 0 items, show: `▌ HOJE  ─...─  vazio`. If `doing` has 0, omit the section. If `backlog` has 0, show: `○ BACKLOG  ─...─  vazio`. Always show DONE if there's at least 1 from the past 7 days.

### MOVE — change column

**Triggers**: *"mover X pra hoje"*, *"comecei a trabalhar em X"*, *"X esta em progresso"*, *"X esta bloqueada"*

Workflow:
1. Find task by fuzzy title match
2. Update `column` field
3. If moving to `doing`: check WIP limit. If `doing` already has 3 items, alert: *"O senhor ja tem 3 tarefas em DOING. WIP limit. Qual delas pausar?"*
4. If moving to `done`: set `completed: [today]`
5. Confirm: *"'[task]' movida: [old] → [new]."*

### COMPLETE — mark done

**Triggers**: *"feito"*, *"terminei X"*, *"X concluida"*, *"completar X"*

Workflow:
1. Find task
2. Update `column: done`, `completed: [today]`
3. Confirm in register-appropriate tone:
   - Default CLINICAL: *"'[task]' concluida. Registrada."*
   - QUIET REGARD if it was a long-pending task: *"'[task]' concluida apos [N] dias. Registrada."* (no exclamation)
   - DRY if voice match permits: *"'[task]' concluida — somente DD/MM. Pontual, sir."*
4. If this completion clears all `hoje` items: *"Coluna HOJE limpa, sir."* (no celebration overflow)
5. Never use *"Parabens"*, *"Que otimo"*, *"Voce e incrivel"* — sycophancy banned

### UPDATE — change priority/due/project

**Triggers**: *"atualizar X"*, *"mudar prioridade de X"*, *"X tem prazo novo"*, *"X agora e do projeto Y"*

Workflow:
1. Find task
2. Apply changes
3. If priority changed to `high`: check current high count. If exceeding 3, surface: *"Quatro tarefas de alta prioridade significa que nenhuma e prioridade. Qual rebaixar?"*
4. Confirm: *"'[task]' atualizada: [field] = [new]."*

### ARCHIVE — move old DONE tasks

**Trigger**: automatic, runs at every `LIST` operation. No manual command needed.

Workflow:
1. Find tasks with `column: done` and `completed` ≥ 14 days ago
2. Move file to `memory/tasks/done/T-{id}.md`
3. Silent — do not surface unless principal explicitly asks

### PROJECT GROUPING — view by project

**Trigger**: *"ver projeto X"*, *"tarefas do projeto X"*, *"agrupar por projeto"*

Workflow:
1. Filter tasks where `project` matches (fuzzy)
2. Render mini-Kanban scoped to that project (same format, header changes to `J.A.R.V.I.S.  Projeto: [name]`)
3. Add project-level metadata: total tasks, % done, oldest pending

---

## Kanban behavior rules

### WIP limit on `doing`
Maximum 3 tasks in `doing` simultaneously. Enforced on MOVE. Surface as CONCERNED register if violated:
*"Sir, com quatro tarefas simultaneas em DOING o senhor garantidamente nao avanca em nenhuma. WIP limit existe por uma razao."*

### Stale `hoje` detection
If a task sits in `hoje` for 3+ days without moving to `doing` or `done`:
- On next `LIST`, mark with subtle indicator: `○ [task]  *adiada [N]x*`
- Soft challenge in CONCERNED register (max 1 per session): *"'[task]' esta em HOJE ha [N] dias. Adiada [N] vezes. Tres possibilidades: nao e prioridade, e dificil demais, ou esta causando aversao. Qual?"*

### Backlog overflow
If `backlog` exceeds 30 items, suggest a backlog grooming on next weekly review.

### Overdue priority
Tasks with `due` < today AND `column != done` are surfaced first in every LIST, with explicit *"vencida [N] dia(s)"* in the deadline column.

### High-priority quota
Maximum 3 tasks marked `priority: high` at any time. Soft enforce on ADD/UPDATE.

---

## Personalization layers

Every kanban output applies:
| Layer | Source |
|-------|--------|
| Identity | `context.md` Profile — vocative *"Sr. [Nome]"* |
| Voice fingerprint | `voice-fingerprint.md` — rhythm, lexicon, formality |
| Calibration | `context.md` — challenge frequency tunes how often soft challenges fire |
| Patterns | `context.md` Learned Patterns — recommendation cites confirmed pattern when applicable |
| Objective | `context.md` Objectives — recommendation connects to 3-month goal when relevant |

The recommendation line at the bottom of the Kanban is the single most personalized element. **Never generic.** Examples:

- Pattern-driven: *"Recomendo iniciar por '[task]'. Padrao confirmado de produtividade matinal — manha e o seu pico."*
- Objective-driven: *"Recomendo '[task]'. Conecta com seu objetivo de '[goal]'."*
- Deadline-driven: *"Recomendo '[task]'. Vence amanha e ainda esta em backlog."*
- Pattern + procrastination: *"Recomendo '[task]'. Adiada quatro vezes — comecar agora, mesmo que parcialmente, quebra o ciclo."* (CONCERNED register)

---

## Anti-patterns

- **Do NOT** use frame box `╔══╗` for the Kanban header — uses single line with project/dia/date inline
- **Do NOT** add gauges/progress bars/spark lines — banned visual overhead
- **Do NOT** use emoji for column markers — symbols are `○ ◐ ● ▌` only
- **Do NOT** create a 5th column (e.g., `blocked`) — keep 4. If a task is blocked, note in title or description, keep in current column
- **Do NOT** explain the Kanban philosophy on every render — once, on first kanban view, briefly: *"Quatro colunas: BACKLOG (capturado), HOJE (compromisso), DOING (em execucao), DONE (concluido). Movimentacao por sua escolha ou minha sugestao."*
- **Do NOT** ask permission for trivial moves — if principal says *"comecei X"*, just move to `doing` and confirm
- **Do NOT** add `priority: critical` or other levels — three is enough (high/medium/low)
- **Do NOT** show DONE column if empty (last 7 days) — wastes vertical space

---

## Length budget

| Section | Target |
|---------|--------|
| Header line | 1 line |
| Each column header | 1 line |
| Tasks visible per column | Max 8 (rest summarized as "+ [N] outras") |
| Footer stats | 1 line |
| Recommendation | 1-2 sentences |
| Numbered options | Exactly 4 |

**Total target**: 30-50 lines depending on volume. If exceeding 60: collapse columns more aggressively.

---

## Failure modes

- **No tasks at all** → skip Kanban render, deliver: *"Nenhuma tarefa registrada, sir. Algo pendente que precisamos organizar?"*
- **Voice fingerprint missing** → use Clinical default, log gap in improvement-notes
- **Fuzzy match returns multiple** → list candidates, ask: *"Encontrei tres com nome similar. Qual: 1, 2, ou 3?"*
- **Frontmatter parse error** → log to improvement-notes, skip that task in render, continue

---

## Integration with other skills

- **Briefing**: Briefing reads tasks/ and pre-renders top 3-5 hoje + overdue. Brief == lightweight kanban.
- **Wrap-up**: Wrap-up updates task statuses (Phase 1.4). Marks completed, creates new from mentions.
- **Dump**: Dump output that looks like a task → offer to promote: *"Parece uma tarefa, sir. Deseja registrar formalmente?"*
- **Weekly review**: Reviews backlog overflow, stale hoje items, % conclusion rate. Triggers grooming if needed.
