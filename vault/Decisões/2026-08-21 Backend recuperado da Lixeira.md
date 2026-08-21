---
data: 2026-08-21
status: decidido
tags: [decisão, backend, apps-script]
---

# Backend recuperado da Lixeira, não reconstruído

**Status:** ✅ Decidido · **PR:** #1 (`claude/apps-script-backup`)

---

## Contexto

Durante a limpeza da obra encerrada, a planilha foi zerada de propósito e o Drive limpo. Como
efeito colateral **não intencional**, o projeto Apps Script do Buildly3 foi apagado junto. O
backend não é versionado por git — o que roda em produção só existe dentro do projeto Google.

Ao retomar o projeto, não havia como testar isso daqui: o ambiente do Claude não tem acesso a
`script.google.com` (bloqueio de rede). Toda a investigação inicial foi por leitura de código.

---

## Alternativas

1. **Reconstruir a partir do contrato observável.** Ler todos os `fetch()` de `pauta.html`,
   `Check-in.html`, `rdo.html` e `buildly-completo.html` e escrever um backend que atenda
   exatamente aquelas chamadas.
2. **Procurar o original.** O projeto Apps Script é um arquivo do Drive por trás dos panos —
   se apagado há menos de ~30 dias, está na Lixeira e pode ser restaurado inteiro.

---

## Decisão

Tentou-se (1) primeiro, produzindo 428 linhas. **(2) prevaleceu:** o usuário encontrou o
original na Lixeira do Google Drive — 1100+ linhas — e ele substituiu a reconstrução.

A diferença de tamanho não era gordura. O original tinha:

- upsert por ID em Pauta e Check-in (a reconstrução só duplicava linha);
- `remover` que apaga a linha de verdade;
- `custos/salvar` gravando nota + itens em abas separadas;
- funções de limpeza de duplicatas;
- **o robô de IA inteiro** (`ia/perguntar`), que a reconstrução nem sabia que existia;
- normalização tolerante de nome de aba, data e status.

Nada disso aparecia nos `fetch()` que dá para ler no front-end.

Única alteração feita sobre o recuperado: a função `errorResponse()`, que não veio na cópia
colada. Foi completada porque o padrão é inequívoco (espelho de `successResponse`, usada em
todo o arquivo). O `appsscript.json` com os `oauthScopes` veio à parte, do usuário.

---

## Consequências

- **Reconstruir backend a partir do front-end é último recurso, não plano A.** O que nenhum
  `fetch()` exercita, some. Registrado em [[Notas/Regras Operacionais Críticas]].
- O `.gs` agora está versionado em `apps-script/BuildlyBackend.gs` — como cópia de referência,
  já que git não implanta Apps Script. Se sumir de novo, pelo menos existe um ponto de partida
  fiel.
- A decisão sobre qual IA usar no robô **já estava tomada dentro do próprio script**: Anthropic
  Claude Haiku, chave em Propriedades do Script. Deixou de ser pendência.

---

## Pendente

Reimplantar e testar contra o Google — não foi possível a partir deste ambiente. Passo a passo
em `apps-script/README.md`. Teste mínimo: criar assunto na Pauta e clicar em atualizar.

---

## Relacionado

- [[Notas/Contrato do Backend]]
- [[Projetos/BUILDLy Premium]]
