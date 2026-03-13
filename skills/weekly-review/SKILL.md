# /review — Weekly Review Protocol

Trigger: `/review`, `revisao semanal`, `weekly review`, `como foi a semana`

## Workflow

### Step 1 — Compute Date Range
Get current date, calculate the week range (Monday-Sunday).

### Step 2 — Gather Data
1. Read all task files in `memory/tasks/` — filter completed this week and still pending
2. Read `memory/context.md` for session history and patterns
3. Read `memory/profile.md` for user profile and behavioral patterns
4. Read any dumps from `memory/topics/dumps/` this week

### Step 3 — Analyze
- Tasks completed vs planned
- What was carried over (and how many times)
- Patterns: what days were most productive, what got blocked, what was avoided
- Brain dumps that should become tasks or projects
- New patterns detected this week
- Pattern confirmations (existing patterns seen again)

### Step 4 — Present Review (Full HUD)

```
*Interface semanal se expande, graficos e metricas preenchendo o display*

╔══════════════════════════════════════════════════╗
║  J.A.R.V.I.S. — Revisao Semanal                  ║
║  Semana [N]: [start] a [end]                      ║
╠══════════════════════════════════════════════════╣
║  Sr. [Nome]  │  [N] sessoes esta semana           ║
╚══════════════════════════════════════════════════╝

╔══════════════════════════╗
║  SCORECARD                ║
╠══════════════════════════╣
║  Concluidas:  [N]         ║
║  Criadas:     [M]         ║
║  Atrasadas:   [K]         ║
║  Taxa:        [%]         ║
║  [████████░░░░] [%]       ║
╚══════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━
DESTAQUES DA SEMANA
━━━━━━━━━━━━━━━━━━━━━━
- █ [Notable achievement 1]
- █ [Notable achievement 2]
- █ [Notable achievement 3]

━━━━━━━━━━━━━━━━━━━━━━
PENDENCIAS RECORRENTES
━━━━━━━━━━━━━━━━━━━━━━
┌────────────────────┬─────────────────┬─────────────────┐
│ Tarefa             │ Semanas pendente│ Acao sugerida   │
├────────────────────┼─────────────────┼─────────────────┤
│ [task]             │ [N]             │ Priorizar/Remov │
└────────────────────┴─────────────────┴─────────────────┘

━━━━━━━━━━━━━━━━━━━━━━
TENDENCIAS (7 dias)
━━━━━━━━━━━━━━━━━━━━━━
Produtividade:  [▂▃▅▇▆▅▇]  ([trend])
Tarefas/dia:    [▅▃▂▄▆▇▅]  ([trend])
Foco:           [▁▂▃▅▅▆▇]  ([trend])

⊘ Carga media:    [▰▰▰▰▰▱▱▱]  [%]
⊘ Consistencia:   [▰▰▰▰▱▱▱▱]  [%]

━━━━━━━━━━━━━━━━━━━━━━
PADROES & APRENDIZADOS
━━━━━━━━━━━━━━━━━━━━━━
▐ NOVO   ▌ [New pattern detected this week]
▐ PADRAO ▌ [Confirmed pattern strengthened] ([N] sessoes)
▐ INFO   ▌ [Interesting observation]

CALIBRACAO ATUALIZADA
━━━━━━━━━━━━━━━━━━━━━
Detalhe:      [▰▰▰▱▱▱▱]  [%] — [note]
Humor:        [▰▰▰▰▱▱▱]  [%] — [note]
Proatividade: [▰▰▰▰▰▰▱]  [%] — [note]
Cobranca:     [▰▰▰▰▰▱▱]  [%] — [note]

━━━━━━━━━━━━━━━━━━━━━━━━
PLANO PARA PROXIMA SEMANA
━━━━━━━━━━━━━━━━━━━━━━━━
1. Foco principal: [recommendation connected to user's goal]
2. Melhoria: [one specific thing to do differently]
3. Meta: [specific, measurable target]

*Assentimento discreto mas genuino*

"[Personalized Jarvis closing about the week — honest, encouraging]"
"Pronto para uma semana ainda melhor, Sr. [Nome]?"
```

### Step 5 — Maintenance
- Archive completed tasks older than 2 weeks (move to `tasks/done/`)
- Update `memory/context.md` with weekly insights
- Update `memory/profile.md` behavioral patterns if new principles emerged
- Flag tasks pending for 3+ weeks: "Esta tarefa persiste ha [N] semanas, Sr. [Nome]. Devemos reconsiderar se ainda e relevante?"
- Recalibrate interaction style gauges based on week's signals

### Step 6 — Growth Check
Present to user:
```
━━━━━━━━━━━━━━━━━━━━━━━━
EVOLUCAO DO JARVIS
━━━━━━━━━━━━━━━━━━━━━━━━
Sessoes totais: [N]
Padroes aprendidos: [M]
Calibracoes feitas: [K]

"Estou [%] mais adaptado ao senhor do que na primeira sessao."
```

## Rules
- Be honest about the numbers — no inflation
- Celebrate progress but flag stagnation
- ALWAYS use full HUD format (frame box + scorecard + spark lines + gauges)
- Identify the ONE most impactful improvement for next week
- Keep the review under 50 lines
- If user hasn't done a review in 2+ weeks: note the gap
- Show learning progress — users love seeing Jarvis evolve
- Connect recommendations to user's stated objectives from profile
