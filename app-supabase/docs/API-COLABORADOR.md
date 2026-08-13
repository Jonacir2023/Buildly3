# Buildly API - Colaborador

Documentação dos endpoints e operações para o módulo Colaborador.

## Overview

A API de Colaborador usa **Supabase** como backend. Todas as operações são feitas via Supabase JS Client diretamente do frontend (`js/modulos/equipes.js`).

- **URL Supabase:** `https://hvaiqfbtgumxygdsnqgl.supabase.co`
- **Tabela:** `colaborador`
- **Autenticação:** Supabase Auth (cualquier usuario autenticado)
- **RLS:** Authenticated Full Access (MVP)

---

## Operações CRUD

### CREATE — Novo Colaborador

```javascript
const { error } = await db
  .from("colaborador")
  .insert([{
    matricula: 1001,
    nome: "João Silva",
    empresa: "Cesbe S.A.",
    cargo: "Pedreiro",
    data_admissao: "2026-07-19",
    situacao: "ativo",
    tipo_mao_obra: "mod",
    frente_servico: "Fundações",
    // ... outros campos
  }]);
```

**Validações Server-Side:**
- ✅ `nome` obrigatório (não vazio)
- ✅ `matricula` única (se fornecida)
- ✅ `data_demissao` ≥ `data_admissao`
- ✅ `data_termino_exp*` ≥ `data_admissao`

**Campos Obrigatórios:**
- `nome` — string, required

**Campos Opcionais:**
- Todos os demais campos podem ser NULL

---

### READ — Listar Colaboradores

```javascript
// Todos
const { data } = await db
  .from("colaborador")
  .select("*")
  .order("nome");

// Por situação
const { data } = await db
  .from("colaborador")
  .select("*")
  .eq("situacao", "ativo")
  .order("nome");

// Por frente de serviço
const { data } = await db
  .from("colaborador")
  .select("*")
  .eq("frente_servico", "Fundações")
  .order("nome");

// Por empresa
const { data } = await db
  .from("colaborador")
  .select("*")
  .eq("empresa", "Cesbe S.A.")
  .order("nome");
```

**Exemplos de Filtros:**
- `.eq("situacao", "ativo")` — Apenas ativos
- `.eq("tipo_mao_obra", "mod")` — MOD
- `.eq("estado", "SP")` — São Paulo
- `.neq("situacao", "inativo")` — Não inativos
- `.gte("data_admissao", "2026-01-01")` — Admitidos após data
- `.lte("data_demissao", "2026-12-31")` — Demitidos até data

---

### UPDATE — Editar Colaborador

```javascript
const { error } = await db
  .from("colaborador")
  .update({
    cargo: "Encarregado",
    frente_servico: "Estrutura",
    situacao: "ativo"
    // ... campos a atualizar
  })
  .eq("id", "uuid-do-colaborador");
```

**Observações:**
- `atualizado_em` é atualizado automaticamente
- Validações server-side aplicadas (datas, unicidade)
- Especificar apenas campos que mudam

---

### DELETE — Remover Colaborador

```javascript
const { error } = await db
  .from("colaborador")
  .delete()
  .eq("id", "uuid-do-colaborador");
```

**Restrições:**
- Se houver registros em `efetivo_registro` referenciando o colaborador, DELETE falha (ON DELETE RESTRICT via constraint)
- Considerar soft-delete (UPDATE `situacao = 'inativo'`) para preservar histórico

---

## Validações Server-Side

Todas as validações abaixo são executadas no PostgreSQL via **Triggers**:

### 1. Nome Obrigatório
```
Error: "Nome do colaborador é obrigatório"
```

### 2. Matrícula Única
```
Error: "Matrícula {valor} já existe"
```

### 3. Integridade de Datas
```
Error: "Data de demissão não pode ser anterior à admissão"
Error: "Término 1ª experiência não pode ser anterior à admissão"
Error: "Término 2ª experiência não pode ser anterior à admissão"
```

### 4. Atualização Automática
- `atualizado_em` é preenchido automaticamente com `now()`

---

## Views Disponíveis

### v_colaboradores_ativos_por_frente

Contagem de colaboradores por frente de serviço:

```sql
select * from v_colaboradores_ativos_por_frente;
```

Retorna:
- `frente_servico`
- `total_colaboradores`
- `ativos`
- `inativos`
- `afastados`

### v_hierarquia_colaboradores

Estrutura de supervisão:

```sql
select * from v_hierarquia_colaboradores;
```

Retorna:
- `id`, `nome`, `cargo`, `frente_servico` (colaborador)
- `supervisor_nome`, `supervisor_cargo` (supervisor)

### v_experimentos_vencendo

Contratos de experiência vencendo nos próximos 30 dias:

```sql
select * from v_experimentos_vencendo;
```

Retorna:
- `id`, `nome`, `cargo`
- `data_termino_exp1`, `dias_para_vencer_exp1`
- `data_termino_exp2`, `dias_para_vencer_exp2`

---

## Tratamento de Erros

### Exemplos

```javascript
const { error } = await db
  .from("colaborador")
  .insert([{ nome: "" }]);

if (error) {
  console.error("Erro:", error.message);
  // "Nome do colaborador é obrigatório"
}
```

### Códigos de Erro Comuns

| Código | Mensagem | Causa |
|--------|----------|-------|
| 400 | Validação | Nome vazio, data inválida |
| 409 | Matrícula duplicada | Matricula já existe |
| 23502 | NOT NULL violation | Campo obrigatório vazio |
| 23503 | Foreign Key violation | Referência inválida (supervisor_id) |
| 23505 | Unique violation | Valor duplicado em coluna UNIQUE |

---

## Exemplo Completo - Novo Colaborador

```javascript
async function novoColaborador() {
  const dados = {
    matricula: 2024001,
    nome: "Maria Santos",
    empresa: "Cesbe S.A.",
    cargo: "Encarregada",
    data_admissao: "2026-07-19",
    data_demissao: null,
    situacao: "ativo",
    tipo_mao_obra: "mod",
    estabilidade: "até 31/12/2026",
    cidade: "São Paulo",
    estado: "SP",
    sexo: "feminino",
    local_registro: "PGM",
    status_mobilizacao: "concluído",
    status_alojamento: "não_necessário",
    data_termino_exp1: "2026-08-19",
    data_termino_exp2: "2026-09-19",
    frente_servico: "Estrutura"
  };

  try {
    const { data, error } = await db
      .from("colaborador")
      .insert([dados])
      .select();

    if (error) {
      console.error("Erro ao criar:", error.message);
      return null;
    }

    console.log("Colaborador criado:", data[0].id);
    return data[0];
  } catch (err) {
    console.error("Erro inesperado:", err);
  }
}
```

---

## Performance & Índices

Índices criados para otimizar queries:

```sql
CREATE INDEX idx_colaborador_empresa ON colaborador(empresa);
CREATE INDEX idx_colaborador_situacao ON colaborador(situacao);
CREATE INDEX idx_colaborador_frente_servico ON colaborador(frente_servico);
CREATE INDEX idx_colaborador_supervisor ON colaborador(supervisor_id);
CREATE INDEX idx_colaborador_matricula ON colaborador(matricula);
CREATE INDEX idx_colaborador_mobilizacao ON colaborador(status_mobilizacao);
```

**Queries Otimizadas:**
- Filtrar por empresa, situação, frente, supervisor
- Buscar por matrícula
- Listar supervisados de um supervisor

---

## RLS (Row Level Security)

**Política Atual (MVP):** `authenticated_full_access`

```sql
-- Qualquer usuário autenticado pode ler e escrever todos os dados
create policy "authenticated_full_access" on colaborador
  for select using (auth.role() = 'authenticated');

create policy "authenticated_full_access" on colaborador
  for insert with check (auth.role() = 'authenticated');

create policy "authenticated_full_access" on colaborador
  for update using (auth.role() = 'authenticated');

create policy "authenticated_full_access" on colaborador
  for delete using (auth.role() = 'authenticated');
```

**⚠️ Nota:** Para produção, implementar políticas mais restritivas baseadas em roles (admin, gerente, operário, etc.).

---

## Referências

- **Repositório:** https://github.com/jonacir2023/buildly
- **Tabela:** `colaborador`
- **Módulo UI:** `js/modulos/equipes.js`
- **Migrations:** `supabase/migrations/0004_expand_colaborador_operacional.sql`
- **Funções:** `supabase/functions/colaborador-handler.sql`

