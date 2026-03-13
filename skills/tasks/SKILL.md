# /tasks — Task Management System

Trigger: `/tasks`, `tarefas`, `task`, `adicionar tarefa`, `listar tarefas`

## Operations

### ADD — Create New Task
When user says "adicionar tarefa", "nova tarefa", "preciso fazer", or similar:

1. Extract: title, priority (ask if unclear), due date (if mentioned), project (if mentioned)
2. Generate ID: `T-{YYYY-MM-DD}-{seq}` (seq = number of tasks created today)
3. Write to `memory/tasks/T-{id}.md`:

```markdown
---
id: T-2026-03-13-1
title: "Task title"
priority: high
status: pending
project: ""
due: 2026-03-15
created: 2026-03-13
---
Task description.
```

4. Confirm: "Registrado, Sr. [Nome]. '[title]' adicionado com prioridade [priority]."
5. For beginners, explain briefly: "Vou lembrar o senhor dessa tarefa no briefing matinal, Sr. [Nome]."

### LIST — Show All Tasks
When user says "listar tarefas", "minhas tarefas", "o que tenho pra fazer":

1. Read all files in `memory/tasks/`
2. Filter: only `status: pending` or `status: in-progress`
3. Sort: high → medium → low, then by due date
4. Present:

```
TAREFAS ATIVAS
━━━━━━━━━━━━━
| # | Tarefa | Prior | Status | Due | Projeto |
|---|--------|-------|--------|-----|---------|
| 1 | ...    | HIGH  | ...    | ... | ...     |

Total: [N] pendentes, [M] em andamento
```

### COMPLETE — Mark Task Done
When user says "completar", "feito", "terminei [task]":

1. Find the task file
2. Update `status: done`
3. Add `completed: {date}` to frontmatter
4. Confirm: "Excelente, Sr. [Nome]. '[title]' concluido."
5. If all high-priority tasks are done: "Todas as prioridades altas foram concluidas, Sr. [Nome]. Impressionante."

### PRIORITIZE — Reorder Priorities
When user says "priorizar", "prioridades", "o que fazer primeiro":

1. Show current high/medium tasks
2. Recommend top 3 based on: due dates > priority > dependencies
3. Ask for confirmation

### UPDATE — Change Task Status/Priority
When user says "atualizar", "mudar prioridade":

1. Find the task
2. Apply changes
3. Confirm the update

## Rules
- Never create duplicate tasks (check existing first)
- If due date is relative ("amanha", "sexta"), convert to absolute date
- Warn when adding a 4th high-priority task: "O senhor ja possui 3 tarefas de alta prioridade, Sr. [Nome]. Recomendo reavaliar."
- When listing, always highlight overdue tasks first
- Keep task titles concise but descriptive
