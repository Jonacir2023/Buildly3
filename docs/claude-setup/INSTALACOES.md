# Setup do Claude Code — 21 instalações

Guia de instalação dos 7 plug-ins, 7 skills e 7 servidores MCP da lista
"21 Coisas Pra Instalar No Claude".

> **Rode estes comandos na SUA máquina**, no Claude Code local.
> Eles não podem ser executados por uma sessão remota: o container é
> efêmero e `/plugin` é um comando interativo do CLI.

## Legenda

| Marca | Significado |
|---|---|
| ✅ | Repositório localizado e confirmado |
| 🟡 | Já presente na sua conta — nada a instalar |
| ⚠️ | **Não confirmado.** Verifique o repo antes de instalar |

---

## 1. Plug-ins

Cada `marketplace add` registra um repositório de terceiros cujo código roda
no seu ambiente. Confira o repo antes de instalar.

### ✅ marketingskills — CRO, copy, SEO, growth
```
/plugin marketplace add coreyhaines31/marketingskills
/plugin install marketingskills@marketingskills
```

### ✅ claude-for-legal — 12 plugins jurídicos (oficial Anthropic)
```
/plugin marketplace add anthropics/claude-for-legal
/plugin install commercial-legal@claude-for-legal
```
Outros: `privacy-legal`, `corporate-legal`.

### ✅ financial-services — banking, PE, equity (oficial Anthropic)
```
/plugin marketplace add anthropics/financial-services
/plugin install financial-analysis@financial-services
```
Instale `financial-analysis` primeiro — ele traz os conectores MCP
compartilhados. Add-ons: investment banking, equity research, private
equity, wealth management.

### ✅ superpowers — metodologia de dev, skills combináveis
```
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```
Mantido por Jesse Vincent. Traz `/brainstorm`, `/write-plan`,
`/execute-plan`.

### ✅ gstack — o setup do Garry Tan, 23 ferramentas
```
/plugin marketplace add garrytan/gstack
```
Papéis: CEO, Designer, Eng Manager, Release Manager, Doc Engineer, QA.

### ✅ repomix — empacota o repo num arquivo pra LLM
**Não é plugin do Claude Code** — é uma CLI:
```
npm install -g repomix     # ou: brew install repomix
repomix                    # empacota o diretório atual
npx repomix --remote owner/repo
```

### ⚠️ claude-skills — "263+ skills"
Nome genérico, vários repos distintos disputam ele. Identifique qual o
autor do carrossel indicava antes de instalar.

---

## 2. Skills

### ✅ caveman — corta tokens de saída
```
/plugin marketplace add JuliusBrussee/caveman
```
Alterna com `/caveman` e "normal mode". O README mede **65% de redução
nos tokens de saída** — entrada e raciocínio não mudam, e a própria skill
custa ~1–1,5k tokens de entrada por turno.

### ⚠️ Não confirmados
`claude-ads`, `humanizer`, `social-media-skills`, `claude-seo`,
`ai-second-brain`, `frontend-design` — não localizei repositório canônico
para nenhum. Peça as URLs ao autor do carrossel antes de instalar.

> `frontend-design` já existe como skill **nativa** do Claude Code. Antes
> de instalar uma versão de terceiro, cheque se a nativa já resolve.

---

## 3. Servidores MCP

### 🟡 Já conectados na sua conta
`google-drive`, `zapier`, `slack` — nada a fazer.

### 🟡 notion — instalado, porém desligado
Está na conta mas aparece como desconectado e desativado neste chat.
Reative em **claude.ai → Settings → Connectors**, e ligue o conector nas
configurações da conversa.

### ✅ perplexity — busca web em tempo real (oficial)
```
claude mcp add perplexity \
  --env PERPLEXITY_API_KEY="sua_chave" \
  -- npx -y @perplexity-ai/mcp-server
```
Exige chave da API Perplexity (serviço pago). O formato de plugin não
carrega segredos — a chave vai por variável de ambiente.

### ✅ agent-browser — automação web econômica em tokens
O `agent-browser` da Vercel é **CLI, não MCP** — é justamente daí que vem
a economia de tokens. Um snapshot de página sai por ~200–400 tokens,
contra ~13,7k do Playwright MCP e ~17k do Chrome DevTools MCP, porque
nenhuma definição de ferramenta ocupa a janela de contexto.

### ⚠️ instagram-mcp
Não localizei repositório canônico. Vale notar que a API do Instagram
restringe bastante publicação e leitura automatizadas — confirme o que o
servidor realmente entrega antes de depender dele.

---

## Sobre os números do carrossel

As contagens não se sustentam: `frontend-design` "277k" não está sequer
em formato de estrelas; `gstack` aparece como "104k★" mas a fonte fala em
~68,2 mil **downloads**; `superpowers` "192k★" está muito acima do repo
real. São números de marketing, com downloads e estrelas misturados.

Isso não invalida os projetos — vários são excelentes e quatro são
oficiais da Anthropic. Só significa que a lista não passou por curadoria
verificada, o que pesa quando cada instalação executa código de terceiro
no seu ambiente. Instale o que você for usar de fato.

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
