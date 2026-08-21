# Backend Apps Script — BuildlyBackend.gs

Cópia de reserva do backend (Google Apps Script) do BUILDLy Premium, recriada
em 2026-08-21 depois que o projeto Apps Script original foi apagado por
engano durante a limpeza da obra encerrada. **Não testada contra o Google**
— o ambiente onde foi escrita não tem acesso a `script.google.com`. Use como
ponto de partida, não como garantia de que bate 100% com o script antigo.

## Como implantar

1. Abra a planilha Buildly3 (`19SDuzU_CLzDRfbNZWJZQzchLDCeQYHgiSC_FxDSdhOw`).
2. Extensões → Apps Script.
3. Apague o conteúdo padrão e cole o de `BuildlyBackend.gs`.
4. Implantar → Nova implantação → tipo **Web app**.
   - Executar como: **Eu**
   - Quem pode acessar: **Qualquer pessoa**
5. Copie a URL terminada em `/exec`.
6. Substitua a URL antiga (`AKfycbwrSC_...`) por essa nova em todos os HTMLs
   que usam `APPS_SCRIPT_URL` / `APPS_SCRIPT_URL_PAUTA` / `APPS_SCRIPT_URL_DIARIO`
   — hoje é a mesma URL nos 5 arquivos: `pauta.html`, `Check-in.html`,
   `rdo.html`, `custos.html`, `buildly-completo.html`.
7. Teste: crie um assunto na Pauta e clique em atualizar. Se salvar sem erro
   e aparecer na aba "Pauta" da planilha, está funcionando.

## O que está implementado

Reconstruído lendo os `fetch()` do front-end (nunca vi o script original):

- `pauta`: `listar` (GET), `criar` (POST), `atualizar-status` (POST)
- `checkin`: `historico` (GET), `salvar` (POST)
- `diario`: `salvar` (POST) — upsert por obra+data, pra RDO não duplicar
  linha a cada salvamento automático
- `backup`: salvar/restaurar snapshot completo do RDO no Google Drive, por
  obra (usado pelo botão "Backup na Nuvem" e ao trocar de aparelho)
- `foto`: upload de foto do RDO pro Drive + leitura em base64

As abas da planilha (`Pauta`, `CheckIn`, `Diario`) são criadas automaticamente
na primeira chamada, com as colunas que este script espera — não precisa
criar headers manualmente antes.

## O que NÃO está implementado (decisão pendente)

- **`ia`/`perguntar`** — o robô que cruzava dados da planilha via IA.
  Precisa decidir qual modelo/API usar e como guardar a chave.
- **`custos`** — `custos.html` já declara a URL do Apps Script mas ainda não
  chama nenhum endpoint (nunca foi ligado). Estrutura de dados pretendida
  está documentada no `README.md` da raiz do repo.
