# 📋 Guia Rápido — Gestão de Equipes

Instruções rápidas para as tarefas mais comuns no módulo Gestão de Equipes.

---

## ➕ Novo Colaborador

1. Clique em **"+ Novo Colaborador"**
2. **Aba 1 (Dados Pessoais):**
   - ✅ Nome (obrigatório)
   - Matrícula
   - Sexo
   - Cidade / UF
   - Cargo
   - Empresa
3. **Aba 2 (Temporal):**
   - Admissão
   - Demissão (opcional)
   - Término 1ª Experiência
   - Término 2ª Experiência
   - Estabilidade
4. **Aba 3 (Operacional):**
   - Situação (ativo/inativo/afastado/licença)
   - Mão de Obra (MOI/MOD/Terceirizado)
   - Frente de Serviço
   - Local de Registro
   - Status Mobilização
   - Status Alojamento
   - Eng. Responsável
   - Supervisor
5. Clique **"Salvar"**

---

## ✏️ Editar Colaborador

1. Na tabela, procure o colaborador
2. Clique **"Editar"** (ícone lápis)
3. Modifique os campos necessários
4. Clique **"Salvar"**

---

## 👁️ Ver Detalhes

1. Clique **"Detalhes"** na tabela
2. Modal mostra todos os 20 campos (read-only)
3. Feche com X

---

## 🗑️ Remover Colaborador

1. Clique **"Remover"** na tabela
2. Confirme no diálogo
3. ⚠️ **Nota:** Só remove se não houver registros de presença (Efetivo)

---

## 🔍 Filtrar & Buscar

### Busca por Nome (em tempo real)
```
Campo: "🔍 Buscar por Nome"
Digite: João
→ Lista filtra enquanto digita
```

### Por Empresa
```
Dropdown: "Empresa"
Selecione: Cesbe S.A.
→ Filtra apenas da empresa selecionada
```

### Por Situação
```
Dropdown: "Situação"
Selecione: Ativo
→ Mostra apenas ativos
```

### Por Frente de Serviço
```
Dropdown: "Frente"
Selecione: Fundações
→ Filtra por frente
```

### Ordenação
```
Dropdown: "Ordenar por"
Opções:
  • Nome (A-Z)
  • Nome (Z-A)
  • Empresa
  • Cargo
  • Data Admissão
```

### Combinar Filtros
Use múltiplos filtros simultaneamente:
```
Empresa: Cesbe S.A.
+ Situação: Ativo
+ Frente: Fundações
= Mostra colaboradores da Cesbe, ativos, na frente Fundações
```

### Limpar Tudo
Clique **"🔄 Limpar Filtros"** para resetar

---

## 📊 Estatísticas

**Seção "Estatísticas"** mostra:
- **Total:** Todos os colaboradores
- **Ativos:** situacao = 'ativo'
- **Inativos:** situacao = 'inativo'
- **MOD:** tipo_mao_obra = 'mod'
- **MOI:** tipo_mao_obra = 'moi'
- **Terceiros:** tipo_mao_obra = 'terceirizado'

---

## ⚠️ Validações

O sistema valida automaticamente:

### Nome Obrigatório
❌ Não salva se nome vazio
→ Mensagem: "Nome é obrigatório"

### Datas Lógicas
❌ Não salva se demissão < admissão
→ Mensagem: "Data de demissão não pode ser anterior à admissão"

### Matrícula Única
❌ Não salva se matrícula já existe
→ Mensagem: "Matrícula já cadastrada"

---

## 🧪 Testar Funcionalidades

Use o checklist interativo em **`tests/test-checklist.html`**:

```
1. Abra no navegador
2. Execute cada teste conforme guia em docs/TESTES-E2E.md
3. Marque ✓ quando passar
4. Progresso salva automaticamente
5. Clique "Exportar" para copiar resultados
```

---

## 🔗 Links Rápidos

- **App:** https://jonacir2023.github.io/buildly/
- **Testes:** `/tests/test-checklist.html`
- **Docs Completo:** `/README.md`
- **Testes Detalhados:** `/docs/TESTES-E2E.md`
- **API Reference:** `/docs/API-COLABORADOR.md`
- **CLAUDE.md:** `/CLAUDE.md` (development)

---

**Data:** 2026-07-19 | **Versão:** 1.0 | **Fase:** 6 (Documentação)
