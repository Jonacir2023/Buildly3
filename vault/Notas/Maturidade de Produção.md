---
criado: 2026-08-21
tags: [nota, produção, ia, avaliação]
---

# Maturidade de Produção

Levantamento feito em 21/08/2026 contra a checklist "demo vs. production" que circula para
aplicações de IA (14 itens). Cada item foi conferido no código, não estimado.

> **Ressalva que muda a leitura:** essa checklist é para produtos **que são IA**. O BUILDLy é um
> app de gestão de obra onde a IA é 1 de 10 módulos. Ler "3/14" como "71% faltando" seria errado
> — boa parte da lista é over-engineering nesta escala. O valor do levantamento está em separar
> o que é lacuna real do que é lacuna irrelevante.

---

## Situação

| # | Item | Status | Realidade |
|---|---|---|---|
| 01 | Frontend | ✅ | 9 apps no GitHub Pages |
| 02 | API Gateway | ⚠️ | Roteamento por `path`/`action`; **sem rate limit** |
| 03 | Authentication | 🟡* | Código de acesso escrito e mesclado, **ainda não ativo** — ver abaixo |
| 04 | Prompt Mgmt | ⚠️ | Hardcoded no `.gs`, mas versionado em git |
| 05 | Model Gateway | ⚠️ | Trocar modelo = 1 constante; sem failover |
| 06 | LLM | ✅ | Claude Haiku, funcionando |
| 07 | RAG | ✅ | `montarContextoParaIA()` busca da planilha antes de responder |
| 08 | Vector DB | ❌ | Desnecessário neste volume |
| 09 | Tools & APIs | ❌ | Zero tools — o robô lê e responde, não age |
| 10 | Memory | ❌ | `messages: [{role:'user'}]` — cada pergunta é isolada |
| 11 | Guardrails | ⚠️ | Só instrução no prompt, sem validar a saída |
| 12 | Observability | ❌ | 8 `Logger.log`; zero tokens, custo ou latência |
| 13 | Evaluation | ❌ | Sem como saber se mexer no prompt melhorou |
| 14 | Deploy & Scale | ⚠️ | Deploy manual, sem CI/CD |

`*` O item 03 estava ❌ quando este levantamento foi feito (21/08). O código foi escrito no mesmo
dia e mesclado em 24/08 — mas **a proteção só passa a valer quando `APP_TOKEN` for criado nas
Propriedades do script**, o que ainda não aconteceu. Hoje o app pede o código e aceita qualquer
coisa. Ver [[Decisões/2026-08-21 Código de acesso ao backend]].

---

## A lacuna que era real: autenticação

O web app é publicado como "qualquer pessoa". Isso é necessário — é o único modo em que o
`fetch()` de uma página estática funciona sem fluxo de login. O problema era não haver nada
depois disso.

A URL `/exec` está dentro do HTML publicado, **em repositório público**. Quem a encontrasse
conseguiria ler pauta, check-in e diário da obra, criar e apagar linhas na planilha, e chamar
`ia/perguntar` sem limite — gastando a chave da Anthropic. Combinado com o item 12
(observabilidade zero), nada disso apareceria.

Corrigido no mesmo dia com um código de acesso. **Um detalhe estrutural que vale guardar:** uma
página estática em repositório público **não consegue guardar segredo nenhum** — qualquer valor
embutido no HTML é público por definição. Todo segredo tem que vir de fora: das Propriedades do
script (servidor) ou digitado pelo usuário (aparelho).

---

## O que vale e o que não vale perseguir

**Vale, e o usuário sentiria:**

- **Memória (10)** — hoje não dá para perguntar "e no mês passado?" logo depois. Um histórico de
  turnos resolve e é barato.
- **Tools (09)** — o robô sabe responder mas não sabe agir. Com tools, criaria uma pauta ou
  lançaria apontamento a partir da conversa.
- **Rate limit no `ia/perguntar` (02)** — o código de acesso protege o perímetro, mas se ele
  vazar a chave volta a ficar exposta. Um teto diário é defesa em profundidade barata.

**Não vale nesta escala:**

- **Vector DB (08)** — só passa a fazer sentido quando 3 meses de dump não couberem mais no
  contexto.
- **Evaluation (13)** e **model gateway com failover (05)** — peso de operação que não se paga
  para uma equipe interna.

---

## Relacionado

- [[Decisões/2026-08-21 Código de acesso ao backend]]
- [[Notas/Contrato do Backend]]
- [[Notas/Regras Operacionais Críticas]]
- [[Projetos/BUILDLy Premium]]
