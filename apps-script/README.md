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
