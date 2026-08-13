# CLAUDE.md — Buildly

## 📍 Informações Críticas do Projeto

**NÃO ESQUECER:**
- Repositório: `https://github.com/jonacir2023/buildly` (renomeado de `buidly` em 2026)
- Caminho local: `/workspace/buildly`
- URL do site: `https://jonacir2023.github.io/buildly/`
- Branch de trabalho: `claude/serene-einstein-em23qs`

---

## 🏗️ Visão Geral do Projeto

**Buildly** é um sistema premium de gestão de obras (controle de obras) baseado em:
- **Backend:** Supabase (PostgreSQL + Auth + RLS)
- **Frontend:** Vanilla HTML/CSS/JS
- **Hospedagem:** GitHub Pages (branch main, raiz /)
- **Banco de dados:** 28 tabelas (UUID PKs, cascading deletes, enums para constrained fields)

**Linguagem:** Português (PT-BR)

---

## 📋 Escopo Atual de Implementação

### Objetivo Principal
Expandir o módulo **Gestão de Equipes** (`js/modulos/equipes.js`) com **20 campos operacionais de canteiro** para o formulário de cadastro de colaboradores.

### Distinção Importante
- **Operacional Canteiro** ← Dados para planejamento, relatórios e operações diárias (ESTE ESCOPO)
- **RH/eSocial** ← Dados de conformidade trabalhista (NÃO incluir - evitar duplicação)

### Os 20 Campos
1. Matrícula
2. Nome
3. Admissão
4. Demissão
5. Situação
6. Cargo
7. Mão de obra (MOI/MOD)
8. Estabilidade
9. Cidade
10. UF
11. Sexo
12. Local de Registro
13. Status Mobilização
14. Término Contr 1ª Experiência
15. Término Contr 2ª Experiência
16. Status de Alojamento
17. Eng Responsável
18. Encarregado/Supervisor
19. Frente de Serviço
20. Empresa

---

## 📁 Estrutura do Projeto

```
/workspace/buildly/
├── index.html                          # Shell principal
├── js/
│   ├── app.js                          # Roteamento e shell base
│   ├── supabase-client.js              # Cliente Supabase
│   ├── vendor/supabase.js              # Biblioteca Supabase
│   └── modulos/
│       ├── equipes.js                  # MÓDULO ALVO - Gestão de Equipes
│       ├── efetivo.js                  # Presença diária (usa colaborador)
│       ├── rdo.js                      # Diário de Obras
│       └── rdo-dashboard.js
├── css/styles.css                      # Estilos globais
├── supabase/
│   ├── migrations/
│   │   ├── 0001_schema_inicial.sql     # Schema com 28 tabelas
│   │   ├── 0002_rls_autenticado.sql    # RLS policies
│   │   └── 0003_seed_obra_inicial.sql  # Dados iniciais
│   └── [future migrations]
└── CLAUDE.md                           # Este arquivo
```

---

## 🔑 Tabela `colaborador` - Estado Atual

**Localização:** `supabase/migrations/0001_schema_inicial.sql` (linhas 31-37)

**Campos Atuais (5):**
- `id` (UUID, PK)
- `nome` (TEXT, obrigatório)
- `empresa` (TEXT)
- `funcao` (TEXT)
- `criado_em` (TIMESTAMPTZ)

**Módulo UI Atual:** `js/modulos/equipes.js` (73 linhas)
- Form com 3 inputs: nome, empresa, funcao
- Lista simples com nome, empresa, funcao
- Botão remover

---

## 🚀 Fases de Implementação

**Status Geral:** 🟢 **83% Concluído (5 de 6 fases)**

### ✅ Fase 1: Database (Concluída)
- [x] Migration `0004_expand_colaborador_operacional.sql` criada
- [x] 6 ENUM types definidos (situacao, tipo_mao_obra, sexo, estado, status_mobilizacao, status_alojamento)
- [x] 20 colunas adicionadas à tabela colaborador com DEFAULT NULL
- [x] 6 índices criados para performance (empresa, situacao, frente_servico, supervisor, matricula, mobilizacao)
- [x] Foreign keys configuradas (supervisor_id auto-referência)
- **Commit:** `67db85a`

### ✅ Fase 2: Backend API (Concluída)
- [x] 3 Funções PL/pgSQL (validar_matricula_unica, validar_datas_colaborador, validar_nome_colaborador)
- [x] 3 Triggers para automação (validação + timestamp)
- [x] 3 Views úteis (v_colaboradores_ativos_por_frente, v_hierarquia_colaboradores, v_experimentos_vencendo)
- [x] Documentação API completa em `docs/API-COLABORADOR.md`
- [x] Exemplos de CRUD em JavaScript
- [x] Guia error handling e RLS
- **Commit:** `95e04b0`

### ✅ Fase 3: Frontend Form (Concluída)
- [x] Modal com 3 abas navegáveis (Pessoal | Temporal | Operacional)
- [x] Todos 20 campos no formulário com validações client-side
- [x] Funcionalidades: novo, editar, detalhes, remover
- [x] Estilos CSS completos para modal, abas e formulário
- [x] Tabela com 7 colunas essenciais (matricula, nome, empresa, cargo, frente, situacao, ações)
- **Commit:** `7b53f50`

### ✅ Fase 4: List View Aprimorado (Concluída)
- [x] Barra de filtros (empresa, situação, frente_servico)
- [x] Busca em tempo real por nome (live search)
- [x] Ordenação customizável (5 opções: nome A-Z, Z-A, empresa, cargo, admissao)
- [x] Dashboard de estatísticas (total, ativos, inativos, MOD, MOI, terceiros)
- [x] Botão limpar filtros
- [x] Re-renderização dinâmica com filtros AND
- **Commit:** `99b7dfc`

### ✅ Fase 5: Testes Integrados (Concluída)
- [x] Documentação E2E completa: `docs/TESTES-E2E.md` (18 casos CT-001 a CT-018)
- [x] Checklist interativo: `tests/test-checklist.html` com:
  - Progress bar visual
  - 18 checkboxes organizados em 4 seções
  - localStorage persistence
  - Estatísticas em tempo real
  - Exportar resultados para clipboard
  - ⏳ **Pendente:** Execução prática dos testes no navegador

### ⏳ Fase 6: Documentação Final (Em Progresso)
- [ ] Atualizar `README.md` com instruções de uso
- [ ] Consolidar documentação em português
- [ ] Atualizar este arquivo com referências completas

**Esforço Total:** ~12 dias (conforme plano)

---

## 🔐 Row Level Security (RLS)

**MVP:** "Authenticated Full Access"
- Qualquer usuário autenticado lê/escreve todos os dados
- Arquivo: `supabase/migrations/0002_rls_autenticado.sql`
- Padrão a ser mantido para novas tabelas

---

## 📝 Convenções de Commit

```
feature: adiciona [descrição]          # novo recurso
feature: atualiza [descrição]          # melhoria
fix: corrige [descrição]               # correção de bug
refactor: [descrição]                  # refatoração
docs: [descrição]                      # documentação
db: [descrição]                        # mudanças de schema
```

---

## 🔗 Links Importantes

- **GitHub:** https://github.com/jonacir2023/buildly
- **GitHub Pages:** https://jonacir2023.github.io/buildly/
- **Supabase Project:** hvaiqfbtgumxygdsnqgl.supabase.co

---

## 📌 Notas para Futuras Sessões

- Sempre verificar este arquivo no início de uma sessão
- O banco de dados Supabase é a fonte única da verdade
- Manter RLS simples (MVP) até que haja requisitos de segurança mais complexos
- Operacional ≠ RH — não duplicar dados de conformidade

