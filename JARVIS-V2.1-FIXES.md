# JARVIS v2.1 — Fixes pendentes

> Audit do Quinn (QA) + filtro do Alan Nicolas em 2026-05-01.
> Bloqueio: NAO entregar pros amigos antes desses fixes.
> Ordem de execucao validada pelo Alan.

---

## P1 — Pre-deploy (must-fix, ~30 min total)

### [ ] 1. install.sh nao copia `dashboard/` (CRITICAL)
- **Sintoma**: amigo roda `bash install.sh`, abre Claude Code, digita `/dash` → erro "Arquivos do dashboard ausentes"
- **Fix**:
  - Adicionar passo `[5/5] Copiando dashboard/` no install.sh
  - Copiar `dashboard/server.py` e `dashboard/index.html` para destino apropriado
  - Criar wrapper `~/.local/bin/jarvis` (executavel) que faz `cd ~/jarvis && claude`
  - Mensagem final do install diz: *"Pra usar: digite `jarvis` em qualquer terminal."*
- **Test**: ambiente limpo, rodar install, depois `jarvis` → /dash funciona

### [ ] 2. Modo de instalacao ambiguo (HIGH)
- **Sintoma**: install.sh copia CLAUDE.md pro `~/.claude/` global. Se amigo abrir Claude Code em outra pasta, JARVIS persona ativa mas `memory/tasks/` nao existe → alucinacao
- **Fix**:
  - README secao "Setup rapido" declara explicitamente: usar via wrapper `jarvis` (criado pelo install)
  - Modo manual fica como nota tecnica avancada, com warning sobre escopo
  - Wrapper `jarvis` resolve: sempre faz cd na pasta certa antes de chamar claude
- **Test**: amigo simulado roda `jarvis` em qualquer pasta → JARVIS abre com memory acessivel

### [ ] 3. YAML escape de aspas duplas (HIGH)
- **Sintoma**: title=`O "melhor" relatorio` salvo como `title: "O "melhor" relatorio"` — YAML invalido. Parser sobrevive por sorte (slice 1:-1), mas pode corromper
- **Fix em `dashboard/server.py` `_render_kv`**:
  ```python
  if isinstance(v, str):
      if k in ("title", "project") or any(c in v for c in [":", "#", '"']):
          escaped = v.replace('\\', '\\\\').replace('"', '\\"')
          return f'{k}: "{escaped}"'
      return f"{k}: {v}"
  ```
  Tambem ajustar parser pra desfazer o escape no read.
- **Test**: `curl POST title='He said "hi"'` → arquivo gerado com `title: "He said \"hi\""` valido

---

## P2 — Polish (~15 min total)

### [ ] 4. briefing/SKILL.md linha 36 — classificacao HOJE obsoleta
- **Sintoma**: skill ainda fala em coluna `HOJE` (modelo v2.0). Coluna nao existe mais
- **Fix**: substituir classificacao por filtro `due == today` independente de coluna. Vencidas via `due < today AND column NOT IN [feitos, descartado]`

### [ ] 5. weekly-review/SKILL.md — 4 referencias a BACKLOG/HOJE/DOING/DONE
- **Linhas**: 57, 58, 74, 222
- **Fix**: substituir pelas 4 colunas v2.1: `a-fazer / fazendo / feitos / descartado`

### [ ] 6. server.py — sem max_length no title
- **Sintoma**: title 300 chars salva, quebra UI no Kanban
- **Fix**: validar `len(title) <= 200` em POST e PATCH. 400 com `"Title too long (max 200)"` se ultrapassar
- **Bonus**: adicionar `maxlength="200"` no input do modal HTML

### [ ] 7. Deletar `templates/` (Alan veto Anti-Hype)
- **Diretiva**: `templates/daily-plan.md` e `templates/weekly-review.md` nao sao referenciados em skill nenhuma. Codigo morto
- **Fix**: `rm -rf templates/` + remover linha do diagrama de estrutura no README

---

## Apos os fixes — protocolo de validacao

1. Rodar todos os 14 testes do Quinn novamente (curl POST/PATCH/DELETE com edge cases)
2. Em ambiente limpo: clonar repo, rodar `bash install.sh`, depois `jarvis`, depois `/dash`
3. Drag-and-drop num card → verificar que arquivo `.md` foi reescrito corretamente
4. Toggle dark mode → verificar persist no localStorage
5. Commit unico: `"fix: install.sh + YAML escape + skill consistency + remove dead templates"`
6. Push pro origin/master

---

## NAO FAZER (Alan veto absoluto)

- ❌ Adicionar rate-limit no server.py
- ❌ Adicionar CORS headers
- ❌ Adicionar file watcher pra auto-refresh
- ❌ Adicionar testes automatizados (overhead pra projeto pessoal de 14 tasks)
- ❌ Refactor de codigo que ja funciona
- ❌ Atualizar templates/ — deletar e seguir adiante

---

## Estimativa

- P1 (3 fixes): ~30 min
- P2 (4 fixes): ~15 min
- Validacao + commit + push: ~10 min
- **Total: ~55 min de trabalho focado**

Comeca por P1 #1 (install.sh) — bloqueia o resto do deploy. P1 #2 e #3 podem rodar em paralelo. P2 todos paralelos.

---

*Anotado por Pandora Starlight em 2026-05-01 21:xx BRT, apos QA review do Quinn (gate CONCERNS) e diretiva do Alan Nicolas (axiomas 1, 3, 5).*
