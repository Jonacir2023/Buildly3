# MANIFEST — Buildly3 (Repositório Único Consolidado)

Este repositório consolida **todo** o histórico de desenvolvimento da plataforma Buildly,
antes espalhado em múltiplos repositórios (`buildly2`, `buidly`). A partir de agora,
**Buildly3 é a única fonte** para esta plataforma.

## 📦 Conteúdo

### `/` (raiz) — App atual em produção
Origem: `Jonacir2023/buildly2`

- `buildly-completo.html` — App integrado (Pauta + Check-in + RDO + Custos)
- `pauta.html`, `Check-in.html`, `custos.html`, `rdo.html` — Módulos standalone
- Backend: Google Sheets via Google Apps Script
- **Este é o app em uso ativo hoje.**

### `/app-supabase/` — Geração mais recente (Supabase, em desenvolvimento)
Origem: `Jonacir2023/buidly`

- App modular (HTML/CSS/JS + Supabase/Postgres)
- Escopo mais amplo: RDO, efetivo, GED, segurança, estoque, tarefas/atas, orçamento,
  terceiros, Gestão de Equipes (20 campos operacionais)
- Banco relacional real (28 tabelas), RLS, triggers de validação
- 18 casos de teste E2E documentados
- **Vantagem para múltiplas obras:** suporta multi-tenancy nativo via tabela `obra` +
  relacionamentos — Google Sheets não escala bem para isso.
- **Status:** não tem paridade de funcionalidades com o app da raiz ainda — só o
  módulo "Gestão de Equipes" está completo.

## 🔀 Por que dois apps no mesmo repo?

Foram dois desenvolvimentos paralelos da mesma ideia (gestão de obras) que nunca
foram unificados. Consolidamos os dois aqui, lado a lado, sem perder nada, até que
seja tomada uma decisão deliberada sobre qual arquitetura seguir adiante
(provavelmente migração gradual para Supabase se/quando houver necessidade de
gerenciar múltiplas obras simultaneamente).

## 🗑️ Repositórios substituídos por este (candidatos a exclusão futura)

- `Jonacir2023/Buildly2` — conteúdo replicado na raiz deste repo
- `Jonacir2023/buidly` — conteúdo replicado em `/app-supabase/`

## 🚫 Independência do repositório JC

Este repositório é **completamente independente** do repositório `Jonacir2023/JC`
(vault Obsidian de gestão de tarefas). Não deve haver nenhum vínculo técnico entre
os dois — sem submodules, imports, links de deploy compartilhados ou dependências
cruzadas. São sistemas separados.
