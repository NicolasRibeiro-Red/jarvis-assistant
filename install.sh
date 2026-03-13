#!/bin/bash
# J.A.R.V.I.S. — Instalador automatico
# Uso: bash install.sh

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  J.A.R.V.I.S. — Instalador               ║"
echo "║  Just A Rather Very Intelligent System     ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Detectar diretorio do script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Verificar se Claude Code existe
if ! command -v claude &> /dev/null; then
    echo "[!] Claude Code nao encontrado."
    echo "    Instale em: https://claude.com/claude-code"
    echo "    Depois rode este script novamente."
    exit 1
fi

echo "[1/4] Copiando CLAUDE.md..."
mkdir -p ~/.claude
cp "$SCRIPT_DIR/CLAUDE.md" ~/.claude/CLAUDE.md

echo "[2/4] Instalando skills..."
mkdir -p ~/.claude/skills
for skill_dir in "$SCRIPT_DIR"/skills/*/; do
    skill_name=$(basename "$skill_dir")
    mkdir -p ~/.claude/skills/$skill_name
    cp "$skill_dir"SKILL.md ~/.claude/skills/$skill_name/SKILL.md
    echo "    + $skill_name"
done

echo "[3/4] Copiando referencias..."
mkdir -p ~/.claude/references
cp "$SCRIPT_DIR"/references/*.md ~/.claude/references/ 2>/dev/null

echo "[4/4] Criando estrutura de memoria..."
# Memoria fica no projeto onde o usuario vai usar o Claude Code
# Sera criada automaticamente pelo Jarvis na primeira sessao

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  Instalacao concluida!                    ║"
echo "╠══════════════════════════════════════════╣"
echo "║                                           ║"
echo "║  Para iniciar, abra o terminal e digite:  ║"
echo "║                                           ║"
echo "║    claude                                  ║"
echo "║                                           ║"
echo "║  O Jarvis vai se apresentar e perguntar   ║"
echo "║  seu nome para personalizar o servico.    ║"
echo "║                                           ║"
echo "╚══════════════════════════════════════════╝"
echo ""
