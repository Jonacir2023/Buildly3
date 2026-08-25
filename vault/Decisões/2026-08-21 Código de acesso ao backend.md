---
data: 2026-08-21
status: decidido
tags: [decisão, segurança, backend, apps-script]
---

# Código de acesso protege o backend

**Status:** ✅ Decidido · **PR:** #5, mesclado em 24/08 · ⚠️ **ainda não ativo em produção**
(falta criar `APP_TOKEN`)

---

## Contexto

Descoberto ao avaliar o app contra a checklist de produção (ver
[[Notas/Maturidade de Produção]]): o web app do Apps Script é publicado como **"qualquer
pessoa"**, e não havia nada além disso.

Publicar assim é necessário — é o único modo em que o `fetch()` de uma página estática funciona
sem fluxo de login OAuth, que o app não tem. O problema era a ausência da camada seguinte.

A URL `/exec` está dentro do HTML publicado, **em repositório público**. Quem a encontrasse
poderia ler pauta, check-in e diário da obra, criar/alterar/apagar linhas na planilha, e chamar
`ia/perguntar` sem limite — gastando a chave da Anthropic. Com observabilidade zero, nada disso
apareceria.

---

## Alternativas

1. **Mudar a implantação para exigir conta Google.** Quebra o app: o `fetch()` de uma página
   estática receberia redirecionamento de login e falharia por CORS. Não há fluxo de login para
   sustentar isso.
2. **Segredo embutido no HTML.** Inútil — a página é pública e o repositório também. Qualquer
   valor no HTML é público por definição. Seria teatro.
3. **Tornar o repositório privado.** Não resolve: o GitHub Pages continua servindo a página
   publicamente, e "ver código-fonte" no navegador expõe a URL do mesmo jeito.
4. **Código de acesso digitado pelo usuário**, guardado nas Propriedades do script (servidor) e
   no `localStorage` (aparelho).

---

## Decisão

Alternativa 4 — a única em que o segredo **não trafega no material público**. O usuário digita
uma vez por aparelho; o app envia em toda chamada; o backend compara com `APP_TOKEN`.

Duas escolhas de implementação que valem registrar:

**Checagem opcional de propósito.** Enquanto `APP_TOKEN` não existir nas Propriedades do script,
tudo passa como antes. Isso permite implantar backend e front-ends sem nenhuma janela de app
quebrado — a proteção liga no momento em que a propriedade é criada, depois de os aparelhos já
terem o código guardado. Sem isso, haveria um intervalo em que o app estaria no ar e sem
funcionar.

**Injeção por shim sobre `fetch()`, num ponto por arquivo**, em vez de alterar as ~15 chamadas
espalhadas por 4 arquivos. Nenhuma chamada escapa, nem as que forem escritas depois. Dois
detalhes que só apareceram no teste:

- **Só a janela principal pergunta.** Os 7 apps em iframe leem o mesmo `localStorage` (mesma
  origem). Se cada um perguntasse, abrir a casca mostraria 8 caixas de diálogo.
- **`token_invalido` limpa o código guardado e repergunta.** Isso torna a troca de código
  auto-aplicável — muda-se `APP_TOKEN` e cada aparelho se reajusta sozinho na chamada seguinte.
  É também como se revoga o acesso de um aparelho perdido.

Interface: `window.prompt()`. Feio, mas é uma vez por aparelho, funciona em todo navegador e não
exigiu marcação nova em 4 arquivos. Trocar por um modal é melhoria cosmética, não estrutural.

---

## Consequências

- **Regra estrutural:** uma página estática em repositório público não guarda segredo nenhum.
  Todo segredo vem das Propriedades do script ou é digitado pelo usuário. Registrado em
  [[Notas/Regras Operacionais Críticas]].
- Aparelho novo passa a exigir um passo a mais (digitar o código). Aceitável: é uma vez por
  aparelho.
- `custos.html` **não** recebeu a injeção — não chama o backend hoje. Quando `custos/salvar` for
  ligado, ela precisa ir junto, ou as chamadas vão ser barradas.

---

## Pendente

- **Ativar:** implantar o `.gs` e criar `APP_TOKEN` nas Propriedades do script. Mesclar em `main`
  publicou o front-end, mas **não implanta Apps Script** — até esse passo, o app pede o código e
  aceita qualquer coisa, e a planilha continua aberta a quem tiver a URL.
- Confirmar no iPhone que a caixa aparece e que o app segue normal depois.
- **Combinar o código com a equipe antes de ativar.** A caixa foi ao ar em 24/08 sem ninguém
  saber o que digitar; cancelar funciona, mas gera dúvida à toa.
- **Rate limit continua ausente.** O código protege o perímetro, mas quem o tiver chama
  `ia/perguntar` à vontade — se vazar, a chave da Anthropic volta a ficar exposta. Um teto
  diário por aparelho é o próximo passo.

---

## Relacionado

- [[Notas/Maturidade de Produção]]
- [[Notas/Contrato do Backend]]
