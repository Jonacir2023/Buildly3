# 👨‍💻 Guia do Desenvolvedor — Gestão de Equipes

Documentação técnica para desenvolvedores estendendo o módulo Gestão de Equipes.

---

## 📁 Arquivos Principais

### Frontend

**`js/modulos/equipes.js`** (392 linhas)
- Modal com 3 abas (Pessoal | Temporal | Operacional)
- Funções principais:
  - `abrirNovoColaborador()` — abre modal vazio
  - `abrirEditarColaborador(id)` — carrega dados e abre modal
  - `abrirDetalhesColaborador(id)` — modal read-only com 20 campos
  - `salvarColaborador()` — INSERT ou UPDATE
  - `removerColaborador(id)` — DELETE com confirmação
  - `filtrarERefazerlista()` — aplica todos os filtros (AND logic)

**`css/styles.css`** (250+ linhas para Gestão de Equipes)
- Classes: `.modal`, `.tab-btn`, `.tab-content`, `.form-control`, `.tabela-colaboradores`
- Suporta tema claro/escuro via CSS variables

### Backend

**`supabase/migrations/0004_expand_colaborador_operacional.sql`**
- 6 ENUM types
- 20 colunas novas na tabela `colaborador`
- 6 índices para performance
- Foreign key para supervisor_id (self-reference)

**Triggers & Funções (dentro de 0004)**
- `tr_validar_matricula` — garante unicidade
- `tr_validar_datas` — valida sequência temporal
- `tr_validar_nome` — obrigatoriedade de nome

**Views (dentro de 0004)**
- `v_colaboradores_ativos_por_frente` — agregação por frente
- `v_hierarquia_colaboradores` — relacionamentos supervisor
- `v_experimentos_vencendo` — contratos expirando

---

## 🔄 Fluxo de Dados

### Novo Colaborador

```
[Form] 
  → salvarColaborador()
    → supabase.from('colaborador').insert({ ... })
    → validar_nome_colaborador() trigger
    → validar_matricula_unica() trigger
    → validar_datas_colaborador() trigger
  → refazerlista() recarrega tabela
  → listarColaboradores() com filtros
```

### Editar Colaborador

```
[Form com data-colaborador-id]
  → salvarColaborador()
    → if (id) supabase.from('colaborador').update({ ... }).eq('id', id)
    → validar_datas_colaborador() trigger
  → refazerlista() recarrega
```

### Filtros & Busca

```
[Inpute de Filtros]
  → filtrarERefazerlista()
    → listarColaboradores() com WHERE conditions
    → aplicar AND logic entre filtros
    → re-renderiza table com novos handlers
```

---

## 📊 Estrutura da Tabela `colaborador`

### Colunas Novas (Fase 1)

```sql
-- Identificação & Básicos
matricula INTEGER UNIQUE
nome TEXT (já existia, agora obrigatório via trigger)
sexo situacao_enum
cidade TEXT
estado estado_enum
cargo TEXT
empresa TEXT (já existia)

-- Temporal
data_admissao DATE
data_demissao DATE (nullable)
data_termino_exp1 DATE
data_termino_exp2 DATE
estabilidade TEXT

-- Operacional
situacao situacao_enum
tipo_mao_obra tipo_mao_obra_enum
frente_servico TEXT
local_registro TEXT
status_mobilizacao status_mobilizacao_enum
status_alojamento status_alojamento_enum

-- Relacionamentos
eng_responsavel_id UUID (FK para users - comentada no migration)
supervisor_id UUID (FK auto-ref para colaborador, ON DELETE SET NULL)

-- Auditoria
atualizado_em TIMESTAMPTZ (ON UPDATE SET CURRENT_TIMESTAMP)
```

### ENUM Types

```sql
situacao_enum: 'ativo', 'inativo', 'afastado', 'licença'
tipo_mao_obra_enum: 'moi', 'mod', 'terceirizado'
sexo_enum: 'masculino', 'feminino', 'não_informado'
estado_enum: 27 estados brasileiros + DF
status_mobilizacao_enum: 'não_iniciado', 'em_progresso', 'concluído', 'cancelado'
status_alojamento_enum: 'não_necessário', 'necessário', 'fornecido', 'recusado'
```

---

## 📝 Exemplos de API (JavaScript)

### Criar Colaborador

```javascript
async function criarColaborador(dados) {
  try {
    const { data, error } = await supabase
      .from('colaborador')
      .insert([{
        matricula: dados.matricula,
        nome: dados.nome,
        empresa: dados.empresa,
        cargo: dados.cargo,
        sexo: dados.sexo,
        cidade: dados.cidade,
        estado: dados.estado,
        data_admissao: dados.data_admissao,
        data_demissao: dados.data_demissao,
        data_termino_exp1: dados.data_termino_exp1,
        data_termino_exp2: dados.data_termino_exp2,
        estabilidade: dados.estabilidade,
        situacao: dados.situacao,
        tipo_mao_obra: dados.tipo_mao_obra,
        frente_servico: dados.frente_servico,
        local_registro: dados.local_registro,
        status_mobilizacao: dados.status_mobilizacao,
        status_alojamento: dados.status_alojamento,
        supervisor_id: dados.supervisor_id
      }])
      .select()
    
    if (error) throw error
    console.log('Colaborador criado:', data[0])
    return data[0]
  } catch (err) {
    console.error('Erro ao criar:', err.message)
  }
}
```

### Listar com Filtros

```javascript
async function listarColaboradores(filtros = {}) {
  let query = supabase.from('colaborador').select('*')
  
  if (filtros.nome) {
    query = query.ilike('nome', `%${filtros.nome}%`)
  }
  if (filtros.empresa) {
    query = query.eq('empresa', filtros.empresa)
  }
  if (filtros.situacao) {
    query = query.eq('situacao', filtros.situacao)
  }
  if (filtros.frente) {
    query = query.eq('frente_servico', filtros.frente)
  }
  
  // Ordenação
  if (filtros.ordem) {
    const [campo, direcao] = filtros.ordem.split('_')
    query = query.order(campo, { ascending: direcao !== 'desc' })
  } else {
    query = query.order('nome')
  }
  
  const { data, error } = await query
  if (error) throw error
  return data
}
```

### Atualizar Colaborador

```javascript
async function atualizarColaborador(id, dados) {
  const { data, error } = await supabase
    .from('colaborador')
    .update(dados)
    .eq('id', id)
    .select()
  
  if (error) throw error
  return data[0]
}
```

### Deletar Colaborador

```javascript
async function deletarColaborador(id) {
  const { error } = await supabase
    .from('colaborador')
    .delete()
    .eq('id', id)
  
  if (error) throw error
}
```

### Consultar View (Colaboradores Ativos por Frente)

```javascript
async function listarAtiosPorFrente() {
  const { data, error } = await supabase
    .from('v_colaboradores_ativos_por_frente')
    .select('*')
  
  if (error) throw error
  return data
}
```

---

## ⚠️ Tratamento de Erros

### Validações Server-Side

```javascript
try {
  // Inserção que viola constraint
  await supabase
    .from('colaborador')
    .insert([{ matricula: 2026001, nome: 'João' }])
} catch (err) {
  // Possíveis erros:
  // - "violates unique constraint" → matrícula duplicada
  // - "data_demissao não pode ser anterior a data_admissao" → validação trigger
  // - "Nome não pode estar vazio" → validação trigger
  console.error('Erro de validação:', err.message)
}
```

### Integração com Efetivo

```javascript
// Verifica se pode remover (sem registros de presença)
async function podeRemoverColaborador(colaborador_id) {
  const { data, error } = await supabase
    .from('efetivo_registro')
    .select('id', { count: 'exact', head: true })
    .eq('colaborador_id', colaborador_id)
  
  return data.length === 0
}
```

---

## 🎨 Componentes CSS Principais

### Modal

```css
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: none; /* JS sets to flex */
}

.modal-content {
  background: var(--cor-superficie);
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}
```

### Abas

```css
.tabs {
  display: flex;
  gap: 0;
  border-bottom: 2px solid var(--cor-borda);
  margin-bottom: 20px;
}

.tab-btn {
  padding: 12px 20px;
  cursor: pointer;
  border: none;
  background: transparent;
  color: var(--cor-texto-fraco);
}

.tab-btn.active {
  color: var(--cor-primaria);
  border-bottom: 3px solid var(--cor-primaria);
}

.tab-content {
  display: none;
}

.tab-content.active {
  display: block;
}
```

### Tabela

```css
.tabela-colaboradores {
  width: 100%;
  border-collapse: collapse;
  background: var(--cor-superficie);
}

.tabela-colaboradores tbody tr:hover {
  background: var(--cor-hover);
}

.tabela-colaboradores td {
  padding: 12px;
  border-bottom: 1px solid var(--cor-borda);
}
```

---

## 🧪 Testes Automatizados (Futuro)

### Exemplo com Playwright

```javascript
import { test, expect } from '@playwright/test'

test('criar novo colaborador', async ({ page }) => {
  await page.goto('https://jonacir2023.github.io/buildly/')
  
  // Clique novo
  await page.click('button:has-text("Novo Colaborador")')
  
  // Preencha aba 1
  await page.fill('input[name="nome"]', 'João Silva')
  await page.fill('input[name="matricula"]', '2026001')
  
  // Clique aba 2
  await page.click('button.tab-btn:has-text("Temporal")')
  await page.fill('input[name="data_admissao"]', '2026-07-19')
  
  // Salve
  await page.click('button:has-text("Salvar")')
  
  // Verifique
  await expect(page.locator('table >> text=João Silva')).toBeVisible()
})
```

---

## 📋 Checklist de Desenvolvimento

- [ ] Entender fluxo de dados (novo → edit → list → delete)
- [ ] Estudar ENUM types e constraints
- [ ] Testar triggers de validação
- [ ] Verificar filtros AND logic
- [ ] Testar responsividade (mobile, tablet, desktop)
- [ ] Validar integração com Efetivo (quando implementar)
- [ ] Executar 18 testes E2E (docs/TESTES-E2E.md)

---

**Última Atualização:** 2026-07-19 | **Versão:** 1.0 | **Contato:** /CLAUDE.md
