# Backend Apps Script — BuildlyBackend.gs

Este é o backend **original** (Google Apps Script) do BUILDLy Premium,
restaurado em 2026-08-21 a partir da Lixeira do Google Drive, depois que o
projeto foi apagado por engano durante a limpeza da obra encerrada. Até
essa restauração, o que estava aqui era uma reconstrução parcial (428
linhas) baseada só no que os `fetch()` do front-end deixavam ver — este
arquivo tem 1100+ linhas e é o script de produção de verdade.

Única mudança feita em cima do que foi recuperado: a função `errorResponse()`
no fim do arquivo, que não veio na cópia (só faltava essa — o padrão é óbvio
pelo uso em toda parte e pelo espelho de `successResponse`). Fora isso, é
código-fonte restaurado, não reconstruído — mas **ainda não foi reimplantado
e testado** contra o Google a partir deste repo, então trate como "pronto
pra colar", não como "já confirmado funcionando".

## Como implantar

1. Abra a planilha Buildly3 (`19SDuzU_CLzDRfbNZWJZQzchLDCeQYHgiSC_FxDSdhOw`).
2. Extensões → Apps Script.
3. Apague o conteúdo padrão e cole o de `BuildlyBackend.gs`.
4. Configurações do projeto (⚙️) → marque "Mostrar o arquivo appsscript.json"
   → cole o conteúdo de `appsscript.json` (tem os `oauthScopes` — Sheets,
   Drive e chamada externa, essa última pro robô de IA).
5. Selecione qualquer função no editor → Executar → aprove a autorização.
6. Implantar → Nova implantação → tipo **Web app**.
   - Executar como: **Eu**
   - Quem pode acessar: **Qualquer pessoa**
7. Copie a URL terminada em `/exec`.
8. Substitua a URL antiga (`AKfycbwrSC_...`) por essa nova em todos os HTMLs
   que usam `APPS_SCRIPT_URL` / `APPS_SCRIPT_URL_PAUTA` / `APPS_SCRIPT_URL_DIARIO`
   — hoje é a mesma URL nos 5 arquivos: `pauta.html`, `Check-in.html`,
   `rdo.html`, `custos.html`, `buildly-completo.html`.
9. Para o robô de IA funcionar: Configurações do projeto → Propriedades do
   script → adicione `ANTHROPIC_API_KEY` com uma chave válida da Anthropic.
10. Teste: crie um assunto na Pauta e clique em atualizar. Se salvar sem
    erro e aparecer na aba "Pauta" da planilha, está funcionando.
11. **Só depois que o teste passar**, ligue o código de acesso — passo a passo
    na seção abaixo.

## Código de acesso (APP_TOKEN)

O web app é publicado como "qualquer pessoa" porque é o único modo em que o
`fetch()` de uma página estática funciona sem fluxo de login. Sem mais nada,
quem descobrisse a URL `/exec` — que está dentro do HTML publicado, em
repositório público — poderia ler e alterar a planilha da obra e gastar a chave
da Anthropic chamando `ia/perguntar`.

A trava é um código combinado, guardado em Propriedades do script e enviado
pelo app em toda chamada. **Nunca fica no HTML nem no repositório:** o usuário
digita uma vez por aparelho e o navegador guarda localmente.

### Ligando sem derrubar o app

A checagem é opcional de propósito — enquanto `APP_TOKEN` não existir, tudo
passa como antes. Por isso a ordem importa:

1. Implante o backend e publique os HTMLs (o app continua funcionando
   normalmente, sem pedir código nenhum).
2. Abra o app em cada aparelho que vai usar. Ele pede o código uma vez —
   digite o que você escolheu. Ainda não há validação, mas já fica guardado.
3. **Por último**, em Configurações do projeto → Propriedades do script,
   adicione `APP_TOKEN` com esse mesmo código. A proteção passa a valer na
   hora, e os aparelhos do passo 2 continuam funcionando sem interrupção.

Se inverter a ordem (criar `APP_TOKEN` antes de os aparelhos terem o código),
nada se perde — o app pede o código na primeira falha e volta a funcionar.

### Trocando o código depois

Mude `APP_TOKEN` nas Propriedades do script. Cada aparelho vai receber
`token_invalido` na chamada seguinte, pedir o código novo e seguir. É também
como se revoga o acesso de um aparelho perdido.

### O que ainda não está coberto

- `custos.html` não chama o backend hoje, então não recebeu a injeção do
  código. Quando `custos/salvar` for ligado, ela precisa ir junto.
- Não há limite de chamadas por aparelho. Quem tem o código pode chamar
  `ia/perguntar` à vontade — dentro da equipe é aceitável, mas se o código
  vazar, a chave da Anthropic volta a ficar exposta. Um teto diário é o
  próximo passo natural.

## O que está implementado

- `pauta`: `listar` (GET), `criar`/`atualizar-status`/`remover` (POST) —
  upsert por ID em tudo, remoção apaga a linha de verdade
- `checkin`: `historico` (GET), `salvar`/`remover` (POST)
- `diario`: `salvar`/`carregar`/`lista-mes` — upsert por data+apontador,
  nunca limpa a aba inteira (só cria cabeçalho se estiver genuinamente vazia)
- `custos`: `salvar` — grava a nota em "Notas Fiscais" e os itens em "Itens
  NF" (aba separada, uma linha por item, ligada pelo ID da NF)
- `backup`: snapshot completo do RDO no Drive por obra, mantém os 30 mais
  recentes
- `foto`: upload de foto do RDO pro Drive
- `ia`/`perguntar`: robô que responde perguntas cruzando Diário, Pauta,
  Check-in e Notas Fiscais via API da Anthropic (Claude Haiku) — precisa da
  `ANTHROPIC_API_KEY` configurada (passo 9 acima)
- `limpar-duplicatas` em Diário/Pauta/CheckIn — funções de manutenção
  pontual, rodar manualmente se aparecerem linhas duplicadas

As abas da planilha (`Pauta`, `CheckIn`, `Diário`, `Notas Fiscais`,
`Itens NF`) são resolvidas ignorando acento/maiúscula/plural — não precisa
bater o nome exato.

## O que ainda não está ligado no front-end

- `custos.html` ainda só salva localmente (`localStorage`) — nunca chama
  `path=custos&action=salvar`, mesmo o endpoint já existindo no backend.
  Ligar isso é trabalho separado no front-end, não no script.
