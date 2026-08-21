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
  disso. Ver [[Notas/Como manter este cofre]].

Nada foi testado contra o Google nem em celular real — o ambiente do Claude não alcança
`script.google.com`, e os testes de interface foram em navegador headless.

---

## Fila de desenvolvimento

### Aguardando teste do usuário

- [ ] **PR #1** — implantar o Apps Script restaurado e testar: criar assunto na Pauta → atualizar.
      Passo a passo em `apps-script/README.md`. Inclui configurar `ANTHROPIC_API_KEY`.
- [ ] **PR #2** — foto da NF no iPhone real: confirmar que abre a câmera, não a galeria; e que a
      foto comprimida continua legível.
- [ ] **PR #3** — robô flutuante no celular, incluindo Reunião, Resumo do Tempo, Medição,
      Documentos e Manutenção (não testadas individualmente), e em desktop ≥900px.

### Em aberto

- [ ] **Ligar Custos à planilha.** `custos/salvar` existe no backend; nenhum front-end chama.
      Hoje as notas fiscais vivem só no aparelho.
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

## Independência do repositório JC

`Jonacir2023/JC` é o vault do **diário de obras**, exclusivamente. Este projeto **não** deve ter
vínculo técnico nem documental com ele: sem submodules, imports, deploy compartilhado ou notas
cruzadas. Documentação do Buildly3 mora aqui, neste cofre, dentro do próprio repositório.

---

## Relacionado

- [[Início]]
- [[Notas/Arquitetura do App]]
- [[Notas/Contrato do Backend]]
- [[Notas/Armazenamento Local]]
- [[Notas/Regras Operacionais Críticas]]
- [[Decisões/Índice de Decisões]]
