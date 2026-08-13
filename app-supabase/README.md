# Buildly 🏗️

Hub de gestão de obra: RDO, efetivo, GED, segurança do trabalho, estoque,
tarefas/atas de reunião (com conferência automática contra contrato e
cronograma), orçamento e terceiros/fornecedores, **além de Gestão de Equipes com 20 campos operacionais**.

## 📊 Sobre Gestão de Equipes

O módulo **Gestão de Equipes** gerencia colaboradores com foco em **planejamento operacional de canteiro**, não em conformidade RH.

### 20 Campos Operacionais

| Campo | Tipo | Descrição |
|-------|------|-----------|
| Matrícula | INTEGER | Número único de matrícula |
| Nome | TEXT | Nome completo (obrigatório) |
| Empresa | TEXT | Empresa contratante |
| Cargo | TEXT | Cargo/função operacional |
| Sexo | ENUM | masculino \| feminino \| não_informado |
| Cidade | TEXT | Cidade de trabalho |
| UF | ENUM | Estado (AC, AL, AP, ..., TO) |
| Admissão | DATE | Data de admissão |
| Demissão | DATE | Data de demissão (nullable) |
| Termo. 1ª Exp. | DATE | Término contrato experiência 1 |
| Termo. 2ª Exp. | DATE | Término contrato experiência 2 |
| Estabilidade | TEXT | Status de estabilidade |
| Situação | ENUM | ativo \| inativo \| afastado \| licença |
| Mão de Obra | ENUM | moi \| mod \| terceirizado |
| Frente de Serviço | TEXT | Frente/seção de trabalho |
| Local de Registro | TEXT | Local de registro |
| Status Mobilização | ENUM | não_iniciado \| em_progresso \| concluído \| cancelado |
| Status Alojamento | ENUM | não_necessário \| necessário \| fornecido \| recusado |
| Eng. Responsável | UUID | Referência a engenheiro |
| Supervisor | UUID | Referência a supervisor (auto-ref) |

## Stack

- **Front-end:** HTML/CSS/JS puro, um único `index.html` responsivo (mobile e desktop).
- **Backend:** [Supabase](https://supabase.com) (Postgres + Auth). Schema em `supabase/migrations/`.
- **Hospedagem:** GitHub Pages (branch `main`, raiz `/`)

## 🚀 Rodando Localmente

Qualquer servidor estático serve, por exemplo:

```bash
python3 -m http.server 8000
```

Depois abra `http://localhost:8000`.

## 📁 Como Usar Gestão de Equipes

### Adicionar Novo Colaborador

1. Clique em **"+ Novo Colaborador"**
2. Preencha a aba **"Dados Pessoais"** com informações básicas
3. Clique na aba **"Temporal"** para datas de admissão/demissão
4. Clique na aba **"Operacional"** para dados de canteiro
5. Clique **"Salvar"** → colaborador aparece na lista

### Editar Colaborador

1. Na lista, clique **"Editar"** na linha do colaborador
2. Modal abre com dados preenchidos
3. Modifique os campos desejados
4. Clique **"Salvar"** → tabela atualiza

### Ver Detalhes

1. Na lista, clique **"Detalhes"**
2. Modal abre com todos os 20 campos (read-only)
3. Feche com X ou clique fora

### Remover Colaborador

1. Na lista, clique **"Remover"**
2. Confirme na caixa de diálogo
3. Colaborador é removido (se não houver registros vinculados em "Efetivo")

### Filtrar Colaboradores

Use a **Barra de Filtros** no topo da lista:

- **Buscar por Nome:** digita em tempo real
- **Por Empresa:** seleciona no dropdown
- **Por Situação:** ativo, inativo, afastado, licença
- **Por Frente:** seleciona a frente de serviço
- **Ordenar por:** Nome A-Z, Z-A, Empresa, Cargo, Data Admissão

Clique **"🔄 Limpar Filtros"** para resetar.

### Estatísticas do Dashboard

Na seção **Estatísticas** você vê:
- **Total:** número de colaboradores
- **Ativos:** com situação = "ativo"
- **Inativos:** com situação = "inativo"
- **MOD:** tipo_mao_obra = "mod"
- **MOI:** tipo_mao_obra = "moi"
- **Terceiros:** tipo_mao_obra = "terceirizado"

## 📖 Banco de Dados

O schema fica em `supabase/migrations/`, aplicado em ordem:

1. `0001_schema_inicial.sql` — todas as tabelas (obra, RDO, efetivo, GED, segurança, estoque, contrato/cronograma, tarefas/atas, orçamento, terceiros).
2. `0002_rls_autenticado.sql` — Row Level Security em todas as tabelas.
3. `0003_seed_obra_inicial.sql` — obra inicial (Suzano/ETA).
4. `0004_expand_colaborador_operacional.sql` — Expansão com 20 campos operacionais (Fase 1).

### Validações Automatizadas

O banco de dados valida automaticamente via triggers PL/pgSQL:

- **Matrícula única:** evita duplicatas
- **Datas lógicas:** demissão ≥ admissão, término experiências após admissão
- **Nome obrigatório:** evita colaboradores sem nome

### Criando um Usuário de Login

O app usa `supabase.auth.signInWithPassword`. Para criar um usuário, use o painel do Supabase: **Authentication → Users → Add user** (marque "Auto Confirm User"). Não crie usuários via SQL direto em produção.

## 🧪 Testes

### Executar Testes Manualmente

Abra `tests/test-checklist.html` no navegador para um checklist interativo com:
- 18 casos de teste (CT-001 a CT-018)
- Progress bar visual
- localStorage para persistência entre sessões
- Exportar resultados

Ou siga o guia detalhado em `docs/TESTES-E2E.md` com instruções passo-a-passo.

### Casos de Teste Inclusos

- **CT-001 a CT-004:** Fluxos principais (novo, editar, detalhes, remover)
- **CT-005 a CT-007:** Validações (nome, datas, matrícula única)
- **CT-008 a CT-014:** Filtros e busca (nome, empresa, situação, frente, ordenação, combinados, estatísticas)
- **CT-015 a CT-018:** UX e integração (navegação abas, responsividade, tema claro/escuro, integração com Efetivo)

## 📚 Documentação Técnica

- **CLAUDE.md** — Guia para desenvolvimento futuro (tecnologia, convenções, fases)
- **docs/API-COLABORADOR.md** — Referência completa API com exemplos CRUD
- **docs/TESTES-E2E.md** — Casos de teste detalhados com prerequisites e passos
- **tests/test-checklist.html** — Checklist interativo para tracking de testes

## 🔐 Segurança

**MVP:** "Authenticated Full Access"
- Qualquer usuário autenticado lê/escreve todos os dados
- Padrão definido em `supabase/migrations/0002_rls_autenticado.sql`
- Pode ser refinado por tabela conforme requisitos de segurança

## 🎯 Próximos Passos

- [ ] Executar testes (CT-001 a CT-018) via `tests/test-checklist.html`
- [ ] Integrar com módulo "Efetivo" (presença diária)
- [ ] Adicionar filtros avançados (date range, busca por múltiplos campos)
- [ ] Dashboard de relatórios (colaboradores por frente, mobilização, etc)

---

**Última Atualização:** 2026-07-19 | **Versão:** 1.0 | **Status:** 🟢 Fase 5 Concluída
