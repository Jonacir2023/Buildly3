---
criado: 2026-08-21
status: ativo
área: Gestão de Obras
tags: [projeto, buildly, cesbe]
---

# BUILDLy Premium

**Status:** 🟢 Ativo — app pronto para a próxima obra (a anterior foi encerrada e os dados
zerados de propósito).
**Responsável:** Jonacir Cazelli · **Empresa:** Cesbe S.A.

Plataforma de gestão de obra. Páginas HTML/JS estáticas, sem build, publicadas no GitHub Pages,
com Google Sheets + Apps Script como backend.

---

## Endereços

| Item | Valor |
|---|---|
| App | https://jonacir2023.github.io/Buildly3/buildly-completo.html |
| Repositório | `Jonacir2023/Buildly3`, branch `main` |
| Pasta local (Mac) | `~/Buildly3` |
| Planilha | "Buildly3" — `19SDuzU_CLzDRfbNZWJZQzchLDCeQYHgiSC_FxDSdhOw` |
| Backend | Apps Script como web app (`/exec`) — ver [[Notas/Contrato do Backend]] |

Módulos: Pauta, Check-in, RDO, Custos, Reunião, Resumo do Tempo, Medições, Documentos,
Manutenção. Ver [[Notas/Arquitetura do App]].

---

## Como trabalhar neste projeto

- Português, sempre.
- Explicar **o que mudou e por quê** — não só entregar o arquivo.
- Testar antes de entregar.
- **Nunca perder informação já lançada.** Ver [[Notas/Regras Operacionais Críticas]].
- O usuário não faz push. Entrega é `.zip` com scripts Python numerados (idempotentes) que
  editam os HTML por trechos exatos, mais `LEIA-ME.txt` com um comando de uma linha.

---

## Histórico

### 24/08/2026 — Os 5 PRs mesclados; o app mudou, o backend não

Todos os PRs abertos em 21/08 entraram em `main` (`6f159c6`), sem conflito. O `main` mesclado
foi validado por inteiro — não só as branches separadas: sintaxe dos 5 HTMLs, os 11 casos do
backend, os 8 do código de acesso e um teste visual confirmando que robô flutuante, foto da NF
e código de acesso convivem no mesmo `buildly-completo.html`, que era o arquivo tocado por dois
PRs diferentes.

Duas consequências que valem lembrar em qualquer merge futuro:

- **Mesclar publica o app, mas não implanta o backend.** `main` é o que o GitHub Pages serve, então
  as mudanças de HTML ficaram no ar na hora. O `.gs` não: git não implanta Apps Script, e o que
  roda continua sendo o que está colado no editor do Google.
- **A caixa do código de acesso apareceu para a equipe** antes de existir código combinado.
  Inofensiva por desenho (sem `APP_TOKEN`, cancelar ou digitar qualquer coisa segue funcionando —
  caminho testado), mas é uma mudança visível que a equipe vê sem aviso. Numa próxima, combinar o
  código antes de mesclar.

### 21/08/2026 — Retomada: backend recuperado, 3 PRs abertos

Sessão de retomada depois da limpeza da obra encerrada.

- **Backend apagado e recuperado.** O projeto Apps Script tinha sumido junto com a limpeza.
  Reconstruí uma versão parcial a partir do front-end (428 linhas); o usuário achou o original
  na Lixeira do Drive (1100+ linhas) e ele prevaleceu. Ver
  [[Decisões/2026-08-21 Backend recuperado da Lixeira]]. → **PR #1**
- **Nota fiscal: decidido usar a câmera do iPhone**, guardando a foto junto do cabeçalho e dos
  itens. OCR adiado. Ver [[Decisões/2026-08-21 Escaneamento de nota fiscal]]. → **PR #2**
- **Robô de IA passou a aparecer em todas as abas**, como botão flutuante. Ver
  [[Decisões/2026-08-21 Robô de IA visível em todas as abas]]. → **PR #3**
- **Este cofre Obsidian foi criado**, para que a próxima sessão não precise redescobrir nada
  disso. Ver [[Notas/Como manter este cofre]]. → **PR #4**
- **Backend passou a exigir código de acesso.** Avaliando o app contra a checklist de produção
  de IA ([[Notas/Maturidade de Produção]]), apareceu uma lacuna real: a URL `/exec` está no HTML
  publicado, em repositório público, e o web app aceitava qualquer um — dava para ler e alterar
  a planilha da obra e gastar a chave da Anthropic. Ver
  [[Decisões/2026-08-21 Código de acesso ao backend]]. → **PR #5**

Nada foi testado contra o Google nem em celular real — o ambiente do Claude não alcança
`script.google.com`, e os testes de interface foram em navegador headless.

---

## Fila de desenvolvimento

### Bloqueando tudo: implantar o Apps Script

- [ ] **Implantar `apps-script/BuildlyBackend.gs`** no editor do Google e trocar a URL `/exec`
      nos HTMLs. Passo a passo em `apps-script/README.md`. Enquanto isso não acontecer, nada do
      backend novo está no ar — nem o `custos/salvar`, nem o código de acesso, nem o robô com a
      `ANTHROPIC_API_KEY`. **É a pendência que destrava as outras.**
- [ ] **Ativar o código de acesso:** criar `APP_TOKEN` nas Propriedades do script. Até lá o app
      pede o código mas aceita qualquer coisa — o item 03 da
      [[Notas/Maturidade de Produção]] só conta como resolvido depois disso.

### Aguardando confirmação em aparelho real

Já estão no ar (mesclados em 24/08), mas nenhum foi visto num aparelho de verdade:

- [ ] **Foto da NF** — confirmar no iPhone que abre a câmera, não a galeria, e que a foto
      comprimida continua legível para reler a nota.
- [ ] **Robô flutuante** — no celular, incluindo Reunião, Resumo do Tempo, Medição, Documentos e
      Manutenção (não testadas individualmente), e em desktop ≥900px.
- [ ] **Caixa do código de acesso** — confirmar que aparece uma vez e que o app segue normal
      depois.

### Em aberto

- [ ] **Rate limit no `ia/perguntar`.** O código de acesso protege o perímetro, mas quem o tiver
      chama à vontade — se vazar, a chave da Anthropic volta a ficar exposta. Teto diário por
      aparelho. Ver [[Notas/Maturidade de Produção]].
- [ ] **Memória multi-turno no robô.** Hoje cada pergunta é isolada; não dá para dizer "e no mês
      passado?" em seguida. Barato e o usuário sente.
- [ ] **Tools no robô.** Hoje ele responde mas não age — com tools, criaria pauta ou lançaria
      apontamento a partir da conversa.
- [ ] **Ligar Custos à planilha.** `custos/salvar` existe no backend; nenhum front-end chama.
      Hoje as notas fiscais vivem só no aparelho. **Levar o shim do código de acesso junto** —
      `custos.html` ainda não o tem.
- [ ] **OCR de nota fiscal** — depende de escolher API de visão. O robô já usa Anthropic, então
      pode ser o caminho natural.
- [ ] **Implementar `foto&action=base64`** no backend — o `rdo.html` já chama esse endpoint como
      primeira via de exibição de foto, e ele não existe. Não é urgente (há fallback), mas
      resolveria dependência de CORS do Google.

### Decisão futura, sem prazo

- [ ] **Migrar para Supabase?** `/app-supabase/` no mesmo repositório é uma geração paralela do
      mesmo sistema (só o módulo "Gestão de Equipes" completo). Vale considerar se aparecer
      necessidade real de gerenciar várias obras ao mesmo tempo — Sheets não escala bem para
      multi-tenancy. Ver `MANIFEST.md` na raiz.

---

## Projeto fechado em si

O BUILDLy é autocontido: código, backend, planilha e documentação vivem neste repositório e mais
nada. **Toda** documentação do projeto vai para `vault/`, aqui — nunca para outro repositório,
outro cofre ou outra base de notas. Sem submodules, sem imports externos, sem deploy
compartilhado, sem notas cruzadas com outros projetos.

---

## Relacionado

- [[Início]]
- [[Notas/Arquitetura do App]]
- [[Notas/Contrato do Backend]]
- [[Notas/Armazenamento Local]]
- [[Notas/Regras Operacionais Críticas]]
- [[Decisões/Índice de Decisões]]
