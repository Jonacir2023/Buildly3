# Buildly - Testes E2E (End-to-End)

Plano de testes integrados para o módulo Gestão de Equipes com 20 campos operacionais.

**Data:** 2026-07-19  
**Versão:** 1.0  
**Status:** ⏳ Em Execução

---

## 📋 Casos de Teste

### **CT-001: Fluxo Novo Colaborador**

**Pré-requisitos:**
- Sistema logado
- Módulo Gestão de Equipes aberto

**Passos:**

1. Clicar em "+ Novo Colaborador"
   - ✅ Modal deve abrir
   - ✅ Título deve ser "Novo Colaborador"
   - ✅ Aba "Dados Pessoais" deve estar ativa

2. Preencher todos os 20 campos:
   ```
   📋 Dados Pessoais:
   - Matrícula: 2026001
   - Nome: João Silva ✓ (obrigatório)
   - Sexo: Masculino
   - Cidade: São Paulo
   - Estado: SP
   - Cargo: Pedreiro
   - Empresa: Cesbe S.A.

   📅 Temporal:
   - Admissão: 2026-07-19
   - Demissão: (deixar vazio)
   - Término 1ª Exp: 2026-08-19
   - Término 2ª Exp: 2026-09-19
   - Estabilidade: até 31/12/2026

   🏗️ Operacional:
   - Situação: Ativo
   - Mão de obra: MOD
   - Frente: Fundações
   - Local Registro: PGM
   - Mobilização: Concluído
   - Alojamento: Não necessário
   ```

3. Clicar em "Salvar"
   - ✅ Mensagem: "Colaborador criado com sucesso!"
   - ✅ Modal deve fechar
   - ✅ Tabela deve atualizar
   - ✅ Novo colaborador deve aparecer na lista

4. Verificar lista:
   - ✅ "João Silva" aparece na tabela
   - ✅ Matrícula 2026001 visível
   - ✅ Empresa "Cesbe S.A." visível
   - ✅ Cargo "Pedreiro" visível
   - ✅ Situação "Ativo" (badge verde)

**Resultado Esperado:** ✅ PASS

---

### **CT-002: Validação - Nome Obrigatório**

**Pré-requisitos:**
- Modal novo colaborador aberto
- Todos os campos vazios

**Passos:**

1. Deixar campo "Nome" vazio
2. Tentar salvar (clicar "Salvar")
   - ✅ Alerta deve aparecer: "Nome é obrigatório"
   - ✅ Modal deve permanecer aberto
   - ✅ Nenhum registro deve ser criado

**Resultado Esperado:** ✅ PASS

---

### **CT-003: Validação - Data Demissão**

**Pré-requisitos:**
- Modal novo colaborador aberto

**Passos:**

1. Preencher:
   - Nome: Maria Silva
   - Admissão: 2026-07-19
   - Demissão: 2026-06-01 (ANTERIOR à admissão)

2. Tentar salvar
   - ✅ Alerta deve aparecer: "Data de demissão não pode ser anterior à admissão"
   - ✅ Modal deve permanecer aberto

**Resultado Esperado:** ✅ PASS

---

### **CT-004: Validação - Matrícula Única**

**Pré-requisitos:**
- Colaborador com matrícula 2026001 já criado

**Passos:**

1. Criar novo colaborador
2. Preencher:
   - Nome: Outro Nome
   - Matrícula: 2026001 (DUPLICADA)

3. Tentar salvar
   - ✅ Erro no banco de dados: "Matrícula 2026001 já existe"
   - ⚠️ Ou mensagem de erro genérica

**Resultado Esperado:** ✅ PASS (validação server-side)

---

### **CT-005: Fluxo Editar Colaborador**

**Pré-requisitos:**
- Colaborador "João Silva" criado (CT-001)
- Modal fechado

**Passos:**

1. Na tabela, clicar "Editar" na linha de João Silva
   - ✅ Modal deve abrir
   - ✅ Título deve ser "Editar - João Silva"
   - ✅ Todos os campos devem estar preenchidos com dados existentes

2. Modificar campos:
   - Cargo: Pedreiro → Encarregado
   - Situação: Ativo → Afastado
   - Frente: Fundações → Estrutura

3. Clicar "Salvar"
   - ✅ Mensagem: "Colaborador atualizado com sucesso!"
   - ✅ Modal deve fechar
   - ✅ Tabela atualiza

4. Verificar tabela:
   - ✅ Cargo agora mostra "Encarregado"
   - ✅ Frente agora mostra "Estrutura"
   - ✅ Situação ainda é "Ativo" (não mudou? Verificar)

**Resultado Esperado:** ✅ PASS

---

### **CT-006: Fluxo Ver Detalhes**

**Pré-requisitos:**
- Colaborador "João Silva" existe

**Passos:**

1. Na tabela, clicar "Detalhes" na linha de João Silva
   - ✅ Modal deve abrir mostrando todos os 20 campos
   - ✅ Todos os valores devem ser preenchidos corretamente

2. Fechar modal
   - ✅ Clique em X ou fora da modal

**Resultado Esperado:** ✅ PASS

---

### **CT-007: Fluxo Remover Colaborador**

**Pré-requisitos:**
- Colaborador "João Silva" existe
- Nenhum registro de presença vinculado (efetivo_registro)

**Passos:**

1. Na tabela, clicar "Remover" na linha de João Silva
   - ✅ Confirmar: "Tem certeza que deseja remover este colaborador?"

2. Confirmar
   - ✅ Mensagem: "Colaborador removido com sucesso!"
   - ✅ Tabela atualiza
   - ✅ "João Silva" não aparece mais na lista

3. Se houver registros vinculados:
   - ✅ Erro: "Não foi possível remover — ele já tem registros de presença vinculados"

**Resultado Esperado:** ✅ PASS

---

### **CT-008: Filtro - Busca por Nome**

**Pré-requisitos:**
- Múltiplos colaboradores na lista

**Passos:**

1. Digitar "João" no campo "🔍 Buscar por Nome"
   - ✅ Tabela filtra em tempo real
   - ✅ Apenas colaboradores com "João" no nome aparecem

2. Digitar "xyz" (não existe)
   - ✅ Mensagem: "Nenhum colaborador encontrado com esses filtros"

3. Limpar campo
   - ✅ Lista volta ao normal

**Resultado Esperado:** ✅ PASS

---

### **CT-009: Filtro - Por Empresa**

**Pré-requisitos:**
- Colaboradores de múltiplas empresas

**Passos:**

1. Selecionar "Cesbe S.A." no dropdown "Empresa"
   - ✅ Tabela mostra apenas da Cesbe S.A.
   - ✅ Contador atualiza

2. Selecionar outro valor
   - ✅ Tabela filtra corretamente

3. Selecionar "-- Todas --"
   - ✅ Lista volta ao normal

**Resultado Esperado:** ✅ PASS

---

### **CT-010: Filtro - Por Situação**

**Pré-requisitos:**
- Colaboradores com diferentes situações (ativo, inativo, afastado)

**Passos:**

1. Selecionar "Ativo"
   - ✅ Apenas colaboradores com situação "Ativo" aparecem

2. Selecionar "Inativo"
   - ✅ Apenas colaboradores com situação "Inativo" aparecem

3. Ordenação deveria ajustar também

**Resultado Esperado:** ✅ PASS

---

### **CT-011: Filtro - Por Frente de Serviço**

**Pré-requisitos:**
- Colaboradores atribuídos a diferentes frentes

**Passos:**

1. Selecionar "Fundações"
   - ✅ Apenas colaboradores da frente "Fundações" aparecem

2. Selecionar "Estrutura"
   - ✅ Filtra corretamente

**Resultado Esperado:** ✅ PASS

---

### **CT-012: Filtro - Ordenação**

**Pré-requisitos:**
- Múltiplos colaboradores

**Passos:**

1. Selecionar "Nome (Z-A)"
   - ✅ Lista ordenada em ordem reversa (Z→A)

2. Selecionar "Cargo"
   - ✅ Lista ordenada por cargo alfabeticamente

3. Selecionar "Data Admissão"
   - ✅ Lista ordenada por data (mais recentes primeiro)

**Resultado Esperado:** ✅ PASS

---

### **CT-013: Múltiplos Filtros Combinados**

**Pré-requisitos:**
- Múltiplos colaboradores com diferentes atributos

**Passos:**

1. Selecionar:
   - Empresa: "Cesbe S.A."
   - Situação: "Ativo"
   - Frente: "Fundações"

   - ✅ Tabela filtra pela combinação (AND)
   - ✅ Mostra apenas colaboradores da Cesbe, ativos, na frente Fundações

2. Digitar nome em busca
   - ✅ Combina com filtros anteriores

3. Clicar "🔄 Limpar Filtros"
   - ✅ Todos os filtros são zerados
   - ✅ Lista volta ao normal

**Resultado Esperado:** ✅ PASS

---

### **CT-014: Estatísticas Dashboard**

**Pré-requisitos:**
- Múltiplos colaboradores com dados variados

**Passos:**

1. Verificar estatísticas mostradas:
   - Total: contagem correta?
   - Ativos: apenas "situacao = ativo"?
   - Inativos: apenas "situacao = inativo"?
   - MOD: apenas "tipo_mao_obra = mod"?
   - MOI: apenas "tipo_mao_obra = moi"?
   - Terceiros: apenas "tipo_mao_obra = terceirizado"?

   - ✅ Todos os números devem ser precisos

2. Após filtrar (ex: por empresa)
   - ⚠️ **Nota:** Estatísticas devem atualizar? Ou mostrar totais globais?
   - **Definir:** Se devem refletir filtros ou ser globais

**Resultado Esperado:** ⚠️ VERIFICAR COMPORTAMENTO ESPERADO

---

### **CT-015: Navegação Entre Abas**

**Pré-requisitos:**
- Modal novo colaborador aberto

**Passos:**

1. Clicar em "📅 Temporal"
   - ✅ Aba muda para temporal
   - ✅ Campos temporais aparecem
   - ✅ Botão da aba fica destacado

2. Clicar em "🏗️ Operacional"
   - ✅ Aba muda para operacional
   - ✅ Campos operacionais aparecem

3. Voltar para "📋 Dados Pessoais"
   - ✅ Dados preenchidos anteriormente estão preservados

**Resultado Esperado:** ✅ PASS

---

### **CT-016: Responsividade**

**Pré-requisitos:**
- Sistema em navegador

**Passos:**

1. Desktop (1920x1080)
   - ✅ Layout correto
   - ✅ Tabela legível

2. Tablet (768x1024)
   - ✅ Modal responsiva
   - ✅ Filtros reorganizados

3. Mobile (375x667)
   - ✅ Modal adaptada
   - ✅ Tabela scrollável horizontalmente
   - ✅ Botões acessíveis

**Resultado Esperado:** ✅ PASS

---

### **CT-017: Tema Claro/Escuro**

**Pré-requisitos:**
- Sistema com suporte a tema

**Passos:**

1. Alternar para tema claro (se disponível)
   - ✅ Modal com cores claras
   - ✅ Contraste legível

2. Alternar para tema escuro
   - ✅ Modal com cores escuras
   - ✅ Contraste legível
   - ✅ Badges e ícones visíveis

**Resultado Esperado:** ✅ PASS

---

### **CT-018: Integração com Efetivo**

**Pré-requisitos:**
- Novo colaborador criado
- Módulo Efetivo disponível

**Passos:**

1. Ir para módulo "Efetivo"
   - ✅ Novo colaborador aparece na lista de presença

2. Marcar presença do novo colaborador
   - ✅ Checkbox funciona
   - ✅ Registro criado em efetivo_registro

3. Voltar para "Gestão de Equipes"
   - ✅ Colaborador ainda existe

4. Tentar remover colaborador com presença
   - ✅ Erro: "Não foi possível remover — ele já tem registros"

**Resultado Esperado:** ✅ PASS

---

## 📊 Resumo de Testes

| ID | Teste | Status | Nota |
|---|---|---|---|
| CT-001 | Novo Colaborador | ⏳ | |
| CT-002 | Validação Nome | ⏳ | |
| CT-003 | Validação Data | ⏳ | |
| CT-004 | Matrícula Única | ⏳ | |
| CT-005 | Editar | ⏳ | |
| CT-006 | Ver Detalhes | ⏳ | |
| CT-007 | Remover | ⏳ | |
| CT-008 | Busca Nome | ⏳ | |
| CT-009 | Filtro Empresa | ⏳ | |
| CT-010 | Filtro Situação | ⏳ | |
| CT-011 | Filtro Frente | ⏳ | |
| CT-012 | Ordenação | ⏳ | |
| CT-013 | Filtros Combinados | ⏳ | |
| CT-014 | Estatísticas | ⏳ | |
| CT-015 | Navegação Abas | ⏳ | |
| CT-016 | Responsividade | ⏳ | |
| CT-017 | Tema Claro/Escuro | ⏳ | |
| CT-018 | Integração Efetivo | ⏳ | |

---

## 🔍 Como Executar os Testes

### Manual (Recomendado para MVP)

1. Abrir Buildly no navegador: https://jonacir2023.github.io/buildly/
2. Fazer login com credenciais Supabase
3. Ir para "Gestão de Equipes"
4. Seguir passos de cada CT-XXX acima
5. Marcar ✅ PASS ou ❌ FAIL
6. Documentar bugs em issues do GitHub

### Automatizado (Futuro)

```bash
# Com Playwright
npm install @playwright/test
npx playwright test tests/colaborador.spec.ts

# Com Cypress
npx cypress run
```

---

## 🐛 Bugs Encontrados

(Será preenchido durante execução dos testes)

---

## ✅ Checklist Final

- [ ] Todos os 18 CTs executados
- [ ] CT-001 a CT-018 = ✅ PASS
- [ ] Nenhum bugs críticos
- [ ] Documentação atualizada
- [ ] Pronto para Fase 6

