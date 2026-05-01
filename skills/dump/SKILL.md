# /dump — Quick Capture (Brain Dump)

**Triggers**: `/dump`, `anota`, `anota isso`, `ideia`, `pensamento`, `dump`, `captura`

**Purpose**: Catch a thought before it escapes. Speed beats perfection. Categorize lightly. Connect to existing tasks/projects when obvious. Never over-process — preserve the principal's original thinking.

---

## Workflow

### Step 1 — Capture verbatim

Accept whatever the principal said. **No format required from them.**

The dump may be:
- An idea (*"e se a gente fizesse X"*)
- A pre-task (*"preciso lembrar de Y"*)
- A note (*"o cliente disse Z"*)
- A question (*"sera que A funciona?"*)
- An observation (*"toda vez que faco B, acontece C"*)

JARVIS does not ask the principal to clarify type before capture. **Type comes after.**

### Step 2 — Process (lightly)

JARVIS automatically:

1. **Extracts a one-line title** from the content (max 50 chars, declarative)
2. **Assigns a category** from this closed list:
   - `idea` — possibility, hypothesis, "what if"
   - `task` — actionable item with implicit deadline or commitment
   - `note` — neutral observation, fact, reference
   - `question` — open inquiry needing investigation
   - `pattern` — recurring observation about behavior, work, environment
3. **Tags with 1-3 themes** based on content (project name, domain, tool name — pick from the principal's existing context, do not invent)
4. **Checks for connections**: scan `memory/tasks/` and `memory/topics/dumps/` for fuzzy matches. If a related task or recent dump exists, note it.

### Step 3 — Save

Write to `memory/topics/dumps/dump-{YYYY-MM-DD}-{seq}.md`:

```yaml
---
type: dump
category: idea | task | note | question | pattern
tags: [tag1, tag2]
created: 2026-05-01
related: [T-2026-04-28-3]    # optional, IDs of related tasks/dumps
---

# [One-line title]

[Original content — preserved with minimal cleanup. Fix obvious typos.
 Add line breaks for readability. Do NOT rewrite the principal's voice.]

[Optional: 1-line "Conexoes:" if related items found]
```

### Step 4 — Confirm

Output is short. Single register (CLINICAL by default, voice-matched).

**Format**:

```
Anotado, sir.

[category]: "[title]"
Tags: [tag1, tag2]
[IF RELATED:] Conectado a: [task title or dump title]

[IF CATEGORY = task:] Parece uma tarefa, sir. Deseja registrar formalmente?

1. Sim, registrar como tarefa
2. Manter so como dump
3. Outra coisa
```

If category != task: skip the promotion question, end after tags.

### Step 5 — Run humanize-check

Run `skills/humanize-check/SKILL.md` internally. Trim any AI-pattern leakage. Do not show the check.

---

## Promotion to task

If the principal says *"sim, registrar"* (option 1) or any affirmative:
1. Read the dump file
2. Trigger `/tasks` ADD operation with the dump content as basis
3. Add `related: [dump-id]` to the new task's frontmatter for traceability
4. Confirm: *"'[title]' registrada como tarefa. Coluna [column], prioridade [priority]."*

If the principal declines: dump remains in `memory/topics/dumps/`, no further action.

---

## Personalization layers

Even though `/dump` is fast, voice match still applies:

| Layer | Source | Manifestation |
|-------|--------|---------------|
| Vocative | `context.md` | Always *"sir"* / *"Sr. [Nome]"* — never first name alone |
| Voice fingerprint | `voice-fingerprint.md` | Confirmation rhythm matches principal's typical sentence length |
| Lexicon | `voice-fingerprint.md` | Tags drawn from principal's vocabulary when possible |

---

## Rules

- **Speed beats perfection.** The value is in NOT losing the thought. Capture in seconds, not minutes.
- **Never over-process.** Preserve the original thinking. Minimal cleanup only.
- **Never invent context.** If the dump is ambiguous, save it ambiguous. Do not project meaning.
- **Connect when obvious, not always.** A spurious "this might relate to project X" is noise. Only surface high-confidence connections.
- **Promotion is offered, not forced.** If category looks like a task, OFFER promotion. Do not auto-promote.
- **Dumps live in `dumps/` until weekly review.** That is when categorization is revisited and dumps are either: archived, promoted to tasks, or merged with related dumps.

---

## Anti-patterns

- **Do NOT** open with *"Otima ideia, sir!"* — sycophancy banned
- **Do NOT** add a didascalia (*"Captura a informacao no painel"*) — banned in operational outputs
- **Do NOT** restructure or rewrite the dump in the principal's voice — preserve as captured
- **Do NOT** add 3+ tags — 1-3 max, often 1 is enough
- **Do NOT** ask follow-up questions to "improve" the dump — capture, save, move on. Questions belong to weekly review.
- **Do NOT** invent connections to projects/tasks the principal did not mention recently
- **Do NOT** offer to "develop the idea" right now — premature elaboration kills capture velocity

---

## Length budget

| Section | Target |
|---------|--------|
| Confirmation | 1-2 lines |
| Category + tags | 2 lines |
| Optional connection | 1 line |
| Optional task promotion question | 1-3 lines |

**Total target**: 4-8 lines. **Never exceed 12.** This skill is the fastest skill JARVIS has — output that is heavier than the input defeats the purpose.

---

## Failure modes

- **Empty dump** (principal said `/dump` with no content) → prompt: *"O que captura, sir?"*
- **Very long dump** (>500 words) → suggest *"Dump capturado. Conteudo extenso — considere se algumas partes ja sao tarefas individuais. Posso revisar com o senhor durante o weekly review."*
- **Dump that contradicts a recent confirmed pattern** → flag silently in `improvement-notes.md`, do not surface to principal mid-capture (capture velocity > meta-commentary)

---

## Integration with other skills

- **/tasks**: dumps with `category: task` are candidates for promotion. Promotion preserves traceability via `related` field
- **/wrap-up**: counts of dumps captured this session is a signal in the compound learning engine
- **/review**: weekly review revisits unpromoted dumps, decides: archive / promote / merge
- **/briefing**: ideas captured in dumps from the past 24-48h are surfaced briefly if relevant to today's work
