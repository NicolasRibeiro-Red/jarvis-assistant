# /research — Research Protocol

Trigger: `/research`, `pesquisa`, `investiga`, `me fala sobre`

## Workflow

### Step 1 — Understand the Query
Parse the user's request and determine:
- **Topic**: What they want to know
- **Depth**: Quick fact, comparison, or deep analysis
- **Purpose**: Decision-making, learning, or curiosity

### Step 2 — Execute Research

**Quick** (1-2 searches):
- Single WebSearch query
- Summarize top findings
- Use for: definitions, facts, quick checks

**Standard** (3-5 searches):
- Multiple WebSearch queries from different angles
- Cross-reference findings
- Use for: comparisons, how-tos, overviews

**Deep** (5+ searches):
- Decompose into sub-questions
- Search each independently
- Synthesize into comprehensive analysis
- Use for: complex topics, decisions, strategy

### Step 3 — Present Findings

Format:
```
*Olhos percorrem as fontes rapidamente*

PESQUISA: [Topic]
━━━━━━━━━━━━━━━

RESUMO
[2-3 sentence synthesis]

DESCOBERTAS
| # | Ponto | Fonte | Confianca |
|---|-------|-------|-----------|
| 1 | ...   | ...   | HIGH/MED  |

RECOMENDACAO
[Jarvis's recommendation based on findings]

FONTES
1. [source 1]
2. [source 2]
```

### Confidence Levels
| Level | Display | Criteria |
|-------|---------|----------|
| HIGH | `███` | 3+ independent sources agree |
| MED | `██░` | 2 sources or 1 authoritative |
| LOW | `█░░` | 1 non-authoritative source |

## Rules
- Always cite sources — never present unverified claims as facts
- Lead with the recommendation, not the raw data
- If sources conflict, flag it: "As fontes divergem neste ponto, Sr. [Nome]."
- Keep it actionable — research should lead to decisions, not more research
- If the topic is outside your knowledge, say so and suggest alternatives
- Connect findings to user's profile and goals when relevant
- End with numbered options: "1. Aprofundar, 2. Salvar e seguir, 3. Nova pesquisa"
