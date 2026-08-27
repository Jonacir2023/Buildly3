#!/bin/bash
# ============================================================
# BUILDLy — preparo da sessão do Claude Code na web
#
# Deixa a sessão pronta para trabalhar: navegador conferido, app servido numa
# porta conhecida, e os dois verificadores do projeto rodados logo de cara.
#
# Roda só no ambiente remoto. Na máquina do usuário sai na hora, para não
# subir servidor nem mexer em nada no Mac dele.
# ============================================================
set -uo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

RAIZ="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
PORTA="${BUILDLY_PORTA:-8795}"
cd "$RAIZ" || exit 0

echo "── BUILDLy: preparando a sessão ──"

# ---- 1. navegador para os testes ----
# Chromium e o pacote playwright já vêm na imagem. Não reinstalo: baixar
# navegador de novo custa minutos e o ambiente já traz o certo.
if python3 -c "import playwright" 2>/dev/null; then
  echo "  ok    playwright disponível"
else
  echo "  ..    instalando playwright"
  pip install --quiet playwright 2>&1 | tail -1
fi
if [ -d /opt/pw-browsers ]; then
  echo "export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers" >> "${CLAUDE_ENV_FILE:-/dev/null}"
  echo "export PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1"        >> "${CLAUDE_ENV_FILE:-/dev/null}"
  echo "  ok    chromium em /opt/pw-browsers"
else
  echo "  !!    /opt/pw-browsers não existe — os testes vão precisar de navegador"
fi

# ---- 2. o app servido ----
# O projeto não tem build: é HTML estático. Mas abrir por file:// bloqueia as
# integrações, então tudo tem que passar por http. Sobe uma vez só; se a
# sessão for retomada e a porta já estiver de pé, não mexe.
if curl -sf -o /dev/null "http://localhost:${PORTA}/rdo.html" 2>/dev/null; then
  echo "  ok    app já servido na porta ${PORTA}"
else
  nohup python3 -m http.server "$PORTA" --directory "$RAIZ" >/tmp/buildly-http.log 2>&1 &
  for _ in $(seq 1 15); do
    curl -sf -o /dev/null "http://localhost:${PORTA}/rdo.html" 2>/dev/null && break
    sleep 0.4
  done
  if curl -sf -o /dev/null "http://localhost:${PORTA}/rdo.html" 2>/dev/null; then
    echo "  ok    app servido na porta ${PORTA}"
  else
    echo "  !!    não consegui servir o app (ver /tmp/buildly-http.log)"
  fi
fi
echo "export BUILDLY_URL=http://localhost:${PORTA}" >> "${CLAUDE_ENV_FILE:-/dev/null}"

# ---- 3. os verificadores do projeto ----
# Rodam agora, não no fim: se alguma coisa entrou torta entre uma sessão e
# outra, é melhor saber antes de escrever a primeira linha.
if [ -f scripts/verificar_sintaxe.py ]; then
  python3 scripts/verificar_sintaxe.py | tail -2 | sed 's/^/  /'
fi
if [ -f scripts/verificar_isolamento.py ]; then
  python3 scripts/verificar_isolamento.py | grep -E "FALHA|OK —" | sed 's/^/  /'
fi

echo "── pronto. testes: python3 tests/executar.py ──"
exit 0
