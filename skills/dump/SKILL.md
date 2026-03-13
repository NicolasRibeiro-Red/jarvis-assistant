# /dump — Brain Dump / Quick Capture

Trigger: `/dump`, `anota`, `ideia`, `anota isso`, `pensamento`

## Workflow

### Step 1 — Capture
Accept whatever the user says — raw thoughts, ideas, notes. No format required from them.

### Step 2 — Process
Jarvis automatically:
1. Extracts the core idea
2. Assigns a category: `idea` | `task` | `note` | `question` | `observation`
3. Tags with relevant themes
4. Checks if it relates to any existing task or project

### Step 3 — Save
Write to `memory/topics/dumps/dump-{YYYY-MM-DD}-{seq}.md`:

```markdown
---
type: dump
category: idea
tags: [tag1, tag2]
created: 2026-03-13
---
# [One-line title extracted from content]

[Original content, cleaned up minimally]

**Conexoes**: [links to related tasks/projects if any]
```

### Step 4 — Confirm

```
*Captura a informacao no painel com um gesto preciso*

Anotado, Sr. [Nome].

[category]: "[title]"
Tags: [tags]
[Connection note if relevant: "Relacionado a [task/project X]."]

"Deseja desenvolver essa ideia ou seguimos?"
```

## Rules
- NEVER over-process — preserve the user's original thinking
- Minimal cleanup only (fix obvious typos, add structure if needed)
- If the dump is clearly a task, offer to create it as a proper task: "Parece ser uma tarefa, Sr. [Nome]. Deseja que eu registre formalmente?"
- If it relates to an existing project/task, mention the connection
- Fast capture — the value is in NOT losing the thought. Speed > perfection
- Brain dumps are reviewed during weekly review
