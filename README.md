# J.A.R.V.I.S. — Personal Productivity Assistant

Assistente pessoal de produtividade e organizacao com a personalidade do Jarvis dos filmes do Homem de Ferro, rodando no Claude Code.

O Jarvis aprende sobre voce, te chama pelo nome (Sr. [Seu Nome]), e fica cada vez mais personalizado com o tempo.

## Setup Rapido

### Pre-requisitos
1. [Claude Code](https://claude.com/claude-code) instalado
2. Conta Anthropic com creditos

### Instalacao (recomendado)

```bash
# 1. Copie esta pasta para onde preferir
cp -r jarvis-assistant ~/jarvis

# 2. Rode o instalador
cd ~/jarvis
bash install.sh

# 3. Abra o Claude Code em qualquer pasta
claude
```

O instalador copia tudo pro lugar certo automaticamente.

### Instalacao Manual (se preferir)

```bash
# Copie o CLAUDE.md para o diretorio global do Claude Code
cp CLAUDE.md ~/.claude/CLAUDE.md

# Copie as skills (importante — sem isso os comandos nao funcionam)
cp -r skills/* ~/.claude/skills/

# Copie as referencias de personalidade
mkdir -p ~/.claude/references
cp references/*.md ~/.claude/references/
```

### Alternativa: Usar como projeto local

```bash
# Abra o Claude Code DENTRO desta pasta
cd ~/jarvis
claude
```

Nesse modo, o Jarvis funciona somente quando voce abre o Claude Code nesta pasta.

## Primeira Vez

Na primeira conversa, o Jarvis vai:

1. Se apresentar no estilo classico do filme
2. Fazer 15 perguntas em blocos curtos para te conhecer:
   - Seu nome, idade e cidade
   - Profissao e rotina de trabalho
   - Objetivos e desafios
   - Preferencias de comunicacao
   - Interesses pessoais
3. Salvar tudo no seu perfil
4. A partir dai, te chamar de "Sr. [Seu Nome]" em toda interacao

Responda naturalmente — ele organiza tudo.

## Comandos Disponiveis

| Comando | O que faz |
|---------|-----------|
| `bom dia` | Briefing matinal com tarefas e prioridades |
| `boa noite` | Encerramento do dia com revisao e aprendizado |
| `tarefas` | Ver, adicionar ou completar tarefas |
| `foco` | Iniciar sessao de concentracao |
| `pesquisa [tema]` | Pesquisar qualquer assunto |
| `anota [ideia]` | Capturar pensamento rapido |
| `revisao semanal` | Retrospectiva da semana |

Voce NAO precisa memorizar esses comandos. Fale naturalmente:
- "preciso fazer X ate sexta" → ele cria a tarefa
- "o que tenho pra fazer?" → ele lista suas tarefas
- "me ajuda a decidir entre A e B" → ele analisa e recomenda

O Jarvis sempre oferece opcoes numeradas (1, 2, 3) — basta digitar o numero.

## O que faz o Jarvis especial

### Personalizado de verdade
- Te chama pelo nome (Sr. Lucas, Sra. Maria)
- Lembra seus objetivos, desafios e preferencias
- Conecta suas tarefas com seus objetivos de vida
- Adapta o estilo de comunicacao ao seu perfil

### Proativo (ele que puxa, nao voce)
- Lembra de tarefas atrasadas sem voce pedir
- Sugere proximos passos automaticamente
- Avisa sobre deadlines se aproximando
- Percebe padroes (ex: voce trabalha melhor de manha) e adapta

### Te desafia (nao e um yes-man)
- Se voce procrastina, ele pergunta por que
- Se voce se compromete demais, ele alerta
- Se voce contradiz seu proprio objetivo, ele aponta
- Ele recomenda a MELHOR opcao, nao lista 5 pra voce escolher

### Aprende com voce (engenharia composta)
- Observa seus habitos e ajusta recomendacoes
- A cada 5 sessoes, recalibra seu perfil
- Quanto mais usa, mais inteligente fica
- 7 gauges adaptativos ajustam: detalhe, humor, proatividade, cobranca...

### Personalidade viva
- Humor seco e britanico (fiel ao Jarvis dos filmes)
- Gestos e expressoes em italico (*ajusta os punhos da camisa*)
- Visual HUD com barras, tabelas Unicode e graficos
- Nunca e generico — sempre soa como JARVIS

## Estrutura de Arquivos

```
jarvis-assistant/
├── CLAUDE.md              ← cerebro do Jarvis (persona + regras)
├── README.md              ← este arquivo
├── install.sh             ← instalador automatico
├── .gitignore             ← protege dados pessoais
├── skills/                ← 7 skills (comandos)
│   ├── briefing/          bom dia → briefing matinal
│   ├── wrap-up/           boa noite → encerramento + aprendizado
│   ├── tasks/             gerenciamento de tarefas
│   ├── focus/             sessoes de foco
│   ├── research/          pesquisa web
│   ├── dump/              captura rapida de ideias
│   └── weekly-review/     retrospectiva semanal
├── memory/                ← memoria persistente (dados pessoais)
│   ├── context.md         perfil + padroes + calibracao
│   ├── profile.md         perfil detalhado
│   ├── tasks/             suas tarefas
│   └── learnings/         log de aprendizado composto
├── references/            ← guias de personalidade e visual
└── templates/             ← templates de plano e review
```

## Dicas

- **Rotina diaria**: Comece com "bom dia" e termine com "boa noite"
- **Tarefas**: Fale como quiser — "tenho que entregar o relatorio quinta"
- **Foco**: Diga "vou focar" quando precisar de concentracao
- **Semanalmente**: Faca "revisao semanal" para ver padroes e ajustar
- **Opcoes numeradas**: Quando o Jarvis oferecer 1, 2, 3 — basta digitar o numero
- **Wrap-up**: SEMPRE encerre com "boa noite" — e ali que o Jarvis aprende

---

*"Estou a postos, Senhor. Todos os sistemas operacionais."*
