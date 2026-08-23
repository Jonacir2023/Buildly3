# Setup do Claude Code — 21 instalações

Guia para os 7 plug-ins, 7 skills e 7 servidores MCP da lista
"21 Coisas Pra Instalar No Claude".

## Existem dois caminhos de instalação — e a lista mistura os dois

| Caminho | O que instala | Onde |
|---|---|---|
| **A. Customize (claude.ai)** | Catálogo oficial da Anthropic | Menu lateral → Customize |
| **B. CLI do Claude Code** | Repositórios do GitHub | `/plugin marketplace add` |

O passo a passo do autor descreve o **caminho A** e está correto como
mecânica de UI. Mas **os nomes do carrossel dele não estão nesse
catálogo** — são projetos de GitHub, que só entram pelo caminho B.

Verificação feita no catálogo desta conta: buscar por `superpowers`,
`gstack`, `caveman`, `repomix`, `claude-skills`, `marketingskills`,
`claude-ads` e `ai-second-brain` em Plugins retorna apenas
correspondências genéricas (marketing, canva, slack, qodo). Em Skills
retorna **vazio**.

Então: seguir só o print do autor não instala a lista do carrossel.

---

## Caminho A — Customize (claude.ai)

### Conectores (MCP)
Customize → **Connectors** → "Connect" no serviço → autorizar.

### Skills
Customize → **Skills** → "+" → "Browse skills", ou upload de `.zip`.
Exige **"Code execution and file creation"** habilitado nas configurações.

### Plugins
Customize → **Plugins** → "Browse plugins" → "Install".

Duas restrições que valem saber antes:
- Só em planos pagos (Pro, Max, Team, Enterprise).
- Rodam em **Cowork e Code — não no Chat comum**. Se o seu uso é
  conversar no app normal, plugin não vai atuar.

### Equivalentes oficiais que você já tem disponíveis

Quatro itens do carrossel têm equivalente no catálogo oficial. Preferir
estes evita rodar código de terceiro:

| Carrossel | Equivalente oficial | Conteúdo |
|---|---|---|
| marketingskills | **marketing** | CRO, copy, SEO, campanhas, relatórios |
| claude-for-legal | **legal** | contratos, NDA, compliance |
| claude-seo | **searchfit-seo** | 11 skills de SEO + 6 comandos |
| frontend-design | **design** | crítica, a11y, design system, handoff |

Todos estão em Browse plugins, com status `available`.

---

## Caminho B — CLI do Claude Code

Rode na **sua máquina**. Cada `marketplace add` registra um repositório
de terceiros cujo código roda no seu ambiente — confira antes.

### ✅ Repositório confirmado

```
/plugin marketplace add coreyhaines31/marketingskills
/plugin marketplace add anthropics/claude-for-legal      # oficial
/plugin marketplace add anthropics/financial-services    # oficial
/plugin marketplace add obra/superpowers-marketplace
/plugin marketplace add garrytan/gstack
/plugin marketplace add JuliusBrussee/caveman
```

Depois, `/plugin install <nome>@<marketplace>`.

- **financial-services**: instale `financial-analysis` primeiro — traz os
  conectores MCP compartilhados.
- **superpowers**: adiciona `/brainstorm`, `/write-plan`, `/execute-plan`.
- **caveman**: alterna com `/caveman`. O README mede **65% de redução nos
  tokens de saída** — entrada e raciocínio não mudam, e a skill custa
  ~1–1,5k tokens de entrada por turno.

### ⚠️ Sem repositório canônico localizado
`claude-skills`, `claude-ads`, `humanizer`, `social-media-skills`,
`ai-second-brain`, `instagram-mcp`. Peça as URLs ao autor.

---

## Itens que não são plugin nem MCP

**repomix** — CLI npm:
```
npm install -g repomix     # ou: brew install repomix
repomix
npx repomix --remote owner/repo
```

**agent-browser** — o projeto da Vercel é **CLI, não MCP**, e é daí que
vem a economia de tokens: nenhuma definição de ferramenta ocupa a janela
de contexto. Um snapshot de página sai por ~200–400 tokens, contra ~13,7k
do Playwright MCP e ~17k do Chrome DevTools MCP.

---

## Servidores MCP — situação atual da conta

| Servidor | Situação |
|---|---|
| google-drive | ✅ conectado |
| zapier | ✅ conectado |
| slack | ✅ conectado |
| notion | ⚠️ instalado, **desconectado** — reconecte em Customize → Connectors |
| perplexity | ver abaixo |
| instagram-mcp | ⚠️ sem repo canônico |
| agent-browser | não é MCP (ver acima) |

### perplexity (oficial)
```
claude mcp add perplexity \
  --env PERPLEXITY_API_KEY="sua_chave" \
  -- npx -y @perplexity-ai/mcp-server
```
Exige chave da API Perplexity (paga). O formato de plugin não carrega
segredos — a chave vai por variável de ambiente.

---

## Sobre os números do carrossel

Não se sustentam: `frontend-design` "277k" não está em formato de
estrelas; `gstack` aparece como "104k★" mas a fonte fala em ~68,2 mil
**downloads**; `superpowers` "192k★" está muito acima do repo real. São
downloads e estrelas misturados.

Isso não invalida os projetos — vários são bons e alguns são oficiais da
Anthropic. Significa que a lista não passou por curadoria verificada, o
que pesa quando cada instalação executa código de terceiro. Instale o que
for usar de fato, e prefira o equivalente oficial quando existir.

## Fontes

- https://github.com/coreyhaines31/marketingskills
- https://github.com/anthropics/claude-for-legal
- https://github.com/anthropics/financial-services
- https://github.com/obra/superpowers-marketplace
- https://github.com/garrytan/gstack
- https://github.com/yamadashy/repomix
- https://github.com/JuliusBrussee/caveman
- https://github.com/perplexityai/modelcontextprotocol
- https://docs.perplexity.ai/docs/getting-started/integrations/mcp-server
