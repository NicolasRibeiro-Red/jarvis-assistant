# /tasks — Task Management + Kanban Terminal

**Triggers**: `/tasks`, `tarefas`, `task`, `kanban`, `adicionar tarefa`, `listar tarefas`, `o que tenho pra fazer`

**Purpose**: Manage the principal's tasks across the 4-column lifecycle. Default view is a **terminal-native Kanban** (monochrome Geist-style, hairline borders, high density). For the visual browser dashboard with drag-and-drop, see `/dash`.

Both `/tasks` and `/dash` read and write the same source: `memory/tasks/*.md`.

---

## Data model

Each task is a markdown file at `memory/tasks/T-{YYYY-MM-DD}-{seq}.md`:

```yaml
---
id: T-2026-05-01-1
title: "Apresentacao quinta-feira"
column: a-fazer            # a-fazer | fazendo | feitos | descartado
priority: high             # high | medium | low
project: "Cliente X"       # optional, groups visually
due: 2026-05-08            # optional, ISO date
created: 2026-05-01
completed: null            # ISO date when column = feitos
---
[Free-form description body if useful — most tasks need none]
```

**Column = pipeline state. Priority = importance.** They are independent.

| Column | Meaning |
|--------|---------|
| `a-fazer` | Captured, not yet started |
| `fazendo` | Active work in progress |
| `feitos` | Completed (auto-archives 14 days after `completed`) |
| `descartado` | Deliberately not pursued — kept for reference |

Legacy compatibility: tasks created with old schema (`status:` field, or columns `backlog/hoje/doing/done`) are auto-mapped on read:
- `backlog` / `hoje` / `pending` → `a-fazer`
- `doing` / `in-progress` → `fazendo`
- `done` → `feitos`

---

## Operations

### ADD — capture a new task
**Triggers**: principal mentions a deadline, says *"preciso fazer X"*, *"adiciona X"*, *"tenho que..."*

Workflow:
1. Extract: title, priority (infer from urgency cues; ask only if genuinely ambiguous), due date if mentioned, project if mentioned
2. Default column: `a-fazer`. Only place in `fazendo` if the principal explicitly says *"comecando agora"* or similar
3. Generate ID: `T-{YYYY-MM-DD}-{seq}` (seq = number of tasks created today)
4. Write file. Confirm in CLINICAL register, voice-matched:
   *"Registrado. '[title]' — a-fazer, prioridade [priority][, prazo DD/MM]."*

**Anti-duplicate check**: before writing, search existing tasks by title fuzzy match (Levenshtein ≤ 30%). If close match exists, surface it: *"Tarefa similar ja existe: '[existing]'. Substituir, atualizar prazo, ou criar mesmo assim?"*

### LIST — show the Kanban (default view)

**Triggers**: `tarefas`, `kanban`, `listar`, `o que tenho pra fazer`

Workflow:
1. Read all files in `memory/tasks/`
2. Classify by column. Within each column, sort by priority (high → medium → low), then by due date (earliest first), then by `created`
3. Compute counts per column
4. Filter `feitos` to last 7 days; older completions are summarized as `+ [N] anteriores`
5. Render Kanban (see format below)
6. Run humanize-check
7. Deliver

**Render format** (Geist terminal-native — monochrome, hairline, high-density):

```
J.A.R.V.I.S.  Tarefas                                    [Dia], DD/MM

○ A FAZER  ───────────────────────────────────────────────  [N] itens
○ [task title shortened to ~40 chars]              alta    DD/MM
○ [task title]                                     media   hoje
○ [task title]                                     baixa   sem prazo
+ [N] outras

◐ FAZENDO  ──────────────────────────────────────────────  [N] itens
◐ [task title]                                     alta    DD/MM
◐ [task title]                                     media   sem prazo

● FEITOS (7 dias)  ──────────────────────────────────────  [N] itens
● [task title]                                     DD/MM
● [task title]                                     DD/MM

✕ DESCARTADO  ───────────────────────────────────────────  [N] itens
✕ [task title]                                     DD/MM
✕ [task title]                                     DD/MM

[total] tarefas  ·  [N] vencidas  ·  [N] feitas (7 dias)

[Recommendation — 1 sentence, register-appropriate, voice-matched.
 Connect to deadline, objective, or confirmed pattern.]

1. Comecar pela [task]
2. Mover/atualizar tarefa
3. Adicionar tarefa
4. Outra coisa
```

**Visual rules**:
- Symbols: `○` a-fazer, `◐` fazendo, `●` feitos, `✕` descartado
- Separators: only `─` (hairline). Never `═` `╔` `╗` etc — those are AI-pattern overhead
- No emoji, no spark lines, no progress bars, no gauges
- Column headers: `[symbol] NAME  ──...──  [N] itens` — single line
- Density: tasks aligned in 3 columns (title | priority | deadline), monospace handles alignment
- Truncate title at 40 chars + ellipsis. Truncate visible items per column to 8, summarize rest as `+ [N] outras`
- Spacing: 1 blank line between sections (the 24px gap rhythm)

**Empty columns**: show as `[symbol] NAME  ─...─  vazio`. Always show `descartado` only if non-empty (rare). Always show `fazendo` even if empty (signal: nada em progresso agora).

### MOVE — change column

**Triggers**: *"mover X pra fazendo"*, *"comecei a trabalhar em X"*, *"X esta em progresso"*, *"descartar X"*, *"X feita"*, *"X concluida"*

Workflow:
1. Find task by fuzzy title match
2. Update `column` field
3. If moving to `feitos`: set `completed: [today]`
4. If moving away from `feitos`: clear `completed`
5. Confirm in register-appropriate tone:
   - Default CLINICAL: *"'[task]' movida: [old] → [new]."*
   - QUIET REGARD if it was a long-pending task moving to feitos: *"'[task]' concluida apos [N] dias. Registrada."* (no exclamation)
   - DRY if voice match permits and the move is to feitos: *"'[task]' concluida — somente DD/MM. Pontual, sir."*

### COMPLETE — mark done (shortcut)

**Triggers**: *"feito"*, *"terminei X"*, *"X concluida"*, *"completar X"*

Equivalent to MOVE with target `feitos`. Use the same confirmation logic.

If this completion clears all `fazendo` items: *"Coluna FAZENDO vazia, sir."* (no celebration overflow).

### DISCARD — drop without completing

**Triggers**: *"descartar X"*, *"X nao vai acontecer"*, *"cancelar X"*, *"X fora do escopo"*

Equivalent to MOVE with target `descartado`. Confirms with: *"'[task]' descartada. Permanece registrada para referencia."*

Discard is **not** delete. The file stays. To remove permanently, principal must say *"excluir X"* or use the delete UI in `/dash`.

### UPDATE — change priority/due/project/title

**Triggers**: *"atualizar X"*, *"mudar prioridade de X"*, *"X tem prazo novo"*, *"X agora e do projeto Y"*, *"renomear X para Y"*

Workflow:
1. Find task
2. Apply changes
3. If priority changed to `high`: check current high count in `a-fazer` + `fazendo`. If exceeding 3, surface: *"Quatro tarefas de alta prioridade significa que nenhuma e prioridade. Qual rebaixar?"*
4. Confirm: *"'[task]' atualizada: [field] = [new]."*

### DELETE — remove permanently

**Triggers**: *"excluir X"*, *"deletar X"*, *"apagar X"*

Workflow:
1. Find task
2. Confirm intention once: *"Excluir permanentemente '[task]'? Use 'descartar' se quiser apenas marcar como nao-feita."*
3. On confirmation: delete the file
4. Confirm: *"Excluida."*

### ARCHIVE — move old `feitos` to archive

**Trigger**: automatic, runs at every `LIST` operation. No manual command needed.

Workflow:
1. Find tasks with `column: feitos` AND `completed` ≥ 14 days ago
2. Move file to `memory/tasks/done/T-{id}.md`
3. Silent — do not surface unless principal explicitly asks

### PROJECT GROUPING — view by project

**Trigger**: *"ver projeto X"*, *"tarefas do projeto X"*, *"agrupar por projeto"*

Workflow:
1. Filter tasks where `project` matches (fuzzy)
2. Render mini-Kanban scoped to that project (same format, header changes to `J.A.R.V.I.S.  Projeto: [name]`)
3. Add project-level metadata: total tasks, % feitos, oldest a-fazer

---

## Kanban behavior rules

### Soft WIP limit on `fazendo`
There is no hard limit, but if `fazendo` exceeds 4 items at LIST time, surface in CONCERNED register (max 1x per session):
*"Sir, com cinco tarefas simultaneas em FAZENDO o senhor garantidamente nao avanca em nenhuma. Considere mover algumas de volta para A FAZER."*

### Stale `a-fazer` detection
If a task with `priority: high` sits in `a-fazer` for 5+ days without moving:
- On next LIST, mark with subtle indicator: `○ [task]  *parada [N]d*`
- Soft challenge in CONCERNED register (max 1 per session): *"'[task]' esta em A FAZER ha [N] dias com prioridade alta. Tres possibilidades: nao e tao prioridade quanto parecia, e dificil demais, ou esta causando aversao. Qual?"*

### Backlog overflow
If `a-fazer` exceeds 30 items, suggest a backlog grooming on next weekly review.

### Overdue priority
Tasks with `due` < today AND `column` is `a-fazer` or `fazendo` are surfaced first in every LIST, with explicit *"vencida [N] dia(s)"* in the deadline column.

### High-priority quota
Soft cap: 3 tasks marked `priority: high` across `a-fazer` + `fazendo`. Soft enforce on ADD/UPDATE.

### Descartado is permanent
Once a task is descartada, it stays descartada unless the principal explicitly moves it back. This is by design — the column documents decisions to NOT do something.

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
- Deadline-driven: *"Recomendo '[task]'. Vence amanha e ainda esta em A FAZER."*
- Pattern + procrastination: *"Recomendo '[task]'. Adiada quatro vezes — comecar agora, mesmo que parcialmente, quebra o ciclo."* (CONCERNED register)

---

## Anti-patterns

- **Do NOT** use frame box `╔══╗` for the Kanban header — single line with project/dia/date inline
- **Do NOT** add gauges/progress bars/spark lines — banned visual overhead
- **Do NOT** use emoji for column markers — symbols are `○ ◐ ● ✕` only
- **Do NOT** create a 5th column — keep 4. If a task is blocked, note in title or description, keep in current column
- **Do NOT** explain the Kanban philosophy on every render — once, on first kanban view, briefly: *"Quatro colunas: A FAZER, FAZENDO, FEITOS, DESCARTADO. Movimentacao por sua escolha ou minha sugestao."*
- **Do NOT** ask permission for trivial moves — if principal says *"comecei X"*, just move to `fazendo` and confirm
- **Do NOT** add `priority: critical` or other levels — three is enough (high/medium/low)
- **Do NOT** confuse `descartado` with deletion — descartar preserves the record; delete removes it

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

- **/dash**: Visual browser version of this Kanban with drag-and-drop. Same source files. Either skill can be the primary view; they stay in sync because they share `memory/tasks/`.
- **/briefing**: Briefing reads tasks/ and pre-renders top 3-5 a-fazer + overdue. Brief == lightweight kanban.
- **/wrap-up**: Wrap-up updates task statuses (Phase 1.4). Marks completed, creates new from mentions, may move stale fazendo back to a-fazer if abandoned.
- **/dump**: Dump output that looks like a task → offer to promote: *"Parece uma tarefa, sir. Deseja registrar formalmente?"*
- **/review**: Reviews backlog overflow, stale a-fazer items, % feitos rate, descartados pattern. Triggers grooming if needed.
