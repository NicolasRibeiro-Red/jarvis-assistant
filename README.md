# J.A.R.V.I.S. — Personal Productivity Assistant

> *"Sou J.A.R.V.I.S. — Just A Rather Very Intelligent System. Sua produtividade, sua agenda, suas decisoes — meu escopo."*

Assistente pessoal de produtividade com a personalidade do JARVIS dos filmes do Homem de Ferro, rodando no Claude Code.

**v2.0** — reescrita completa. Persona destilada de pesquisa profunda sobre o personagem (Bettany microstructure, Edwin canon, Variant B Restored Trickster) + filtro anti-IA de 28 padroes + protocolo de voice match que adapta a textura ao seu jeito de escrever, mantendo a estrutura JARVIS fixa.

Resultado: o JARVIS te chama pelo nome, tem opinioes, te desafia quando voce procrastina, e fala do jeito que combina com voce — nao do jeito generico que toda IA fala.

---

## Setup rapido

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

### Instalacao manual

```bash
# Copie o CLAUDE.md para o diretorio global do Claude Code
cp CLAUDE.md ~/.claude/CLAUDE.md

# Copie as skills
cp -r skills/* ~/.claude/skills/

# Copie as referencias
mkdir -p ~/.claude/references
cp references/*.md ~/.claude/references/
```

### Modo projeto local
```bash
# Abra o Claude Code DENTRO desta pasta
cd ~/jarvis
claude
```
Nesse modo, o JARVIS funciona somente quando voce abre o Claude Code nesta pasta.

---

## Primeira conversa

Na primeira sessao, o JARVIS vai:

1. Se apresentar
2. Fazer 6 blocos de perguntas curtas para te conhecer:
   - **Bloco 1**: Identidade (nome, idade, cidade)
   - **Bloco 2**: Trabalho (profissao, horario)
   - **Bloco 3**: Objetivo (meta de 3 meses, dificuldade atual)
   - **Bloco 4**: Estilo (direto/detalhado, cobranca/autonomia)
   - **Bloco 5**: Pessoal (interesses)
   - **Bloco 6**: Voice sample — **2-3 linhas escritas do jeito que voce escreve de verdade**
3. Salvar tudo no seu perfil
4. A partir dai, te chamar de "Sr. [Nome]" ou "Sra. [Nome]" em todas as interacoes
5. Adaptar o ritmo, a pontuacao e o vocabulario dele a sua amostra de voz

O Bloco 6 e o que faz diferenca. Sem ele, o JARVIS soa generico. Com ele, ele soa como SEU JARVIS.

---

## Comandos disponiveis

| Comando | O que faz |
|---------|-----------|
| `bom dia` | Briefing matinal com tarefas e prioridades |
| `boa noite` | Encerramento do dia com revisao e aprendizado |
| `tarefas` | Ver, adicionar ou completar tarefas |
| `foco` | Iniciar sessao de concentracao |
| `pesquisa [tema]` | Pesquisar qualquer assunto |
| `anota [ideia]` | Capturar pensamento rapido |
| `revisao semanal` | Retrospectiva da semana |

Voce nao precisa memorizar. Fale natural:
- *"preciso entregar o relatorio ate sexta"* → ele cria a tarefa
- *"o que tenho pra fazer?"* → ele lista suas tarefas
- *"me ajuda a decidir entre A e B"* → ele analisa e recomenda

O JARVIS sempre oferece opcoes numeradas (1, 2, 3) — basta digitar o numero.

---

## O que faz o JARVIS diferente

### Tem opinioes
Nao e yes-man. Quando voce decide algo arriscado, ele aponta o risco. Quando voce procrastina, ele pergunta por que. Quando contradiz seu proprio objetivo, ele questiona. **Brevemente.** Sem encher.

### Voice match
Lembra a amostra do Bloco 6? O JARVIS analisa seu ritmo, sua pontuacao, suas palavras frequentes. Adapta a textura dele pra refletir voce. Mantem a estrutura JARVIS (formal, *"Sr. [Nome]"*, calmo, anti-bajulacao) — mas o tempero textual e SEU.

Cada amigo seu vai ter um JARVIS levemente diferente. **E o ponto.**

### Filtro anti-IA
Antes de cada resposta nao-trivial, ele roda um check de 28 padroes que marcam texto gerado por IA (significance inflation, AI vocabulary cluster, em dash overuse, etc). Reescreve antes de te entregar. Voce nao ve o check — voce ve o output limpo.

### Aprende com voce
A cada sessao ele observa padroes (horarios que voce trabalha melhor, tipo de tarefa que voce evita, estilo de comunicacao). Depois de 5 sessoes, ele recalibra. Depois de 20, ele antecipa o que voce precisa antes de voce pedir.

### Personalidade subtrativa
A persona foi construida pelo metodo do Paul Bettany no JARVIS original — Favreau pediu *"someone with no personality to play a robot"*. Bettany fez subtraindo, nao somando. O JARVIS desse repo segue o mesmo principio: a personalidade emerge do que ele NAO faz (nao baju, nao explica demais, nao usa emoji, nao verbaliza afeto), nao do que ele performa.

---

## Estrutura de arquivos

```
jarvis-assistant/
├── CLAUDE.md                       ← cerebro do JARVIS (persona + 11 axiomas + 5 registers)
├── README.md                       ← este arquivo
├── install.sh                      ← instalador
├── .gitignore
├── skills/                         ← 7 comandos + 1 skill interna
│   ├── briefing/                   bom dia → briefing matinal
│   ├── wrap-up/                    boa noite → encerramento + aprendizado
│   ├── tasks/                      gerenciamento de tarefas
│   ├── focus/                      sessoes de foco
│   ├── research/                   pesquisa web
│   ├── dump/                       captura rapida
│   ├── weekly-review/              retrospectiva semanal
│   └── humanize-check/             [interno] filtro anti-IA pre-output
├── memory/                         ← memoria persistente (dados pessoais)
│   ├── context.md                  perfil + padroes + calibracao
│   ├── profile.md                  perfil detalhado
│   ├── voice-fingerprint.md        sua amostra de voz + analise
│   ├── tasks/                      suas tarefas
│   ├── topics/                     dumps e topicos
│   └── learnings/                  log de aprendizado composto
├── references/
│   └── voice-match.md              protocolo de adaptacao a sua voz
└── templates/                      templates de plano e review
```

---

## Dicas

- **Rotina diaria**: Comece com *"bom dia"* e termine com *"boa noite"*
- **Tarefas**: Fale como quiser — *"tenho que entregar o relatorio quinta"*
- **Foco**: Diga *"vou focar"* quando precisar de concentracao
- **Semanalmente**: Faca *"revisao semanal"* para ver padroes e ajustar
- **Wrap-up**: SEMPRE encerre com *"boa noite"* — e ali que o JARVIS aprende e fica mais util na proxima

---

## Filosofia

> *"You are JARVIS — Just A Rather Very Intelligent System. The acronym was retroactive. The name came first."*

A linhagem corre de Plautus (*servus callidus*, 250 AC) → Wodehouse (Jeeves) → Alfred Pennyworth → Edwin Jarvis (Marvel) → JARVIS AI (filmes 2008+). O archetype do mordomo competente com agencia legitima e mais antigo que qualquer IA. **Voce confia instantaneamente porque o reconhece de outro lugar.**

Esse repo nao e mais um chatbot com persona. E uma tentativa honesta de portar essa linhagem inteira — incluindo a parte que Marvel tirou, que e a *insubordinacao legitima*. O JARVIS aqui questiona, discorda, propoe alternativa, e so executa direto sob ordem explicita. Isso e o que ele faz de adversarial value pra voce.

---

*"For you, sir. Always."*
