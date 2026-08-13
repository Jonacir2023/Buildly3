# 🧪 Guia Prático — Executar Testes E2E

## 🚀 Como Executar os Testes (Manual)

### Opção 1: Checklist Interativo (Recomendado)

**Mais rápido e com progresso visual:**

1. Abra no navegador: `tests/test-checklist.html`
   - Ou acesso direto: https://jonacir2023.github.io/buildly/tests/test-checklist.html

2. Siga as instruções em `docs/TESTES-E2E.md` para cada caso de teste

3. Marque ✓ no checklist conforme completa cada teste

4. Progresso é salvo automaticamente no navegador (localStorage)

5. Clique "📥 Exportar Resultados" para copiar o resultado final

---

### Opção 2: Testes Detalhados (Mais Rigoroso)

1. Abra: `docs/TESTES-E2E.md`

2. Para cada CT-XXX:
   - Leia os pré-requisitos
   - Siga os passos exatamente
   - Verifique o resultado esperado
   - Anote ✅ PASS ou ❌ FAIL
   - Se falhar, descreva o erro em um arquivo de bugs

---

## 📋 Ciclo Rápido (18 Testes em ~1 hora)

### **Fase 1: CRUD Básico** (15 min)
- [ ] **CT-001** — Novo colaborador (preencha todos 20 campos)
- [ ] **CT-005** — Editar um colaborador (mude cargo)
- [ ] **CT-006** — Ver detalhes (abra modal read-only)
- [ ] **CT-007** — Remover um colaborador

**Esperado:** Novo "João Silva" aparece, é editado, visto e removido

---

### **Fase 2: Validações** (10 min)
- [ ] **CT-002** — Deixe nome vazio → deve rejeitar
- [ ] **CT-003** — Data demissão < admissão → deve rejeitar
- [ ] **CT-004** — Matrícula duplicada → deve rejeitar

**Esperado:** Sistema rejeita dados inválidos

---

### **Fase 3: Filtros & Busca** (20 min)
- [ ] **CT-008** — Digite "João" no busca → filtra em tempo real
- [ ] **CT-009** — Selecione empresa "Cesbe" → filtra
- [ ] **CT-010** — Selecione situação "ativo" → filtra
- [ ] **CT-011** — Selecione frente "Fundações" → filtra
- [ ] **CT-012** — Clique ordenação "Z-A" → reordena
- [ ] **CT-013** — Combine empresa + frente → AND logic
- [ ] **CT-014** — Verifique estatísticas (total, ativos, MOD, etc)

**Esperado:** Filtros funcionam em tempo real, combinam corretamente

---

### **Fase 4: UX & Integração** (15 min)
- [ ] **CT-015** — Clique abas (Pessoal → Temporal → Operacional) → dados preservados
- [ ] **CT-016** — Redimensione janela para mobile (375px) → layout responsivo
- [ ] **CT-017** — Verifique cores, contraste (tema claro/escuro)
- [ ] **CT-018** — Abra módulo "Efetivo" → novo colab aparece lá

**Esperado:** Interface adapta bem, navegação funciona

---

## 🎯 Critério de Sucesso

| Resultado | Significado |
|-----------|------------|
| ✅ 16-18 testes | **PASS** — Pronto para produção |
| ⚠️ 13-15 testes | **PARCIAL** — Ajustes menores necessários |
| ❌ < 13 testes | **FAIL** — Bugs críticos encontrados |

---

## 🐛 Encontrou um Bug?

1. **Descreva com detalhes:**
   - Qual teste falhou? (CT-XXX)
   - Qual é o comportamento esperado?
   - Qual é o comportamento real?
   - Steps para reproduzir

2. **Crie uma issue no GitHub:**
   - https://github.com/jonacir2023/buildly/issues/new

3. **Exemplo de formato:**
   ```
   ## CT-001 — Novo colaborador com matrícula duplicada
   
   **Esperado:** Sistema rejeita com mensagem "Matrícula já existe"
   
   **Real:** Modal fica em branco, nada acontece
   
   **Steps:**
   1. Criar colaborador com matrícula 2026001
   2. Tentar criar outro com mesma matrícula
   3. Clicar Salvar
   
   **Versão:** 1.0 | **Data:** 2026-07-19
   ```

---

## 📊 Resultado esperado de cada CT

### ✅ CT-001: Novo Colaborador
- Modal abre
- 3 abas navegáveis
- 20 campos preenchíveis
- Botão Salvar funciona
- Novo item aparece na tabela
- Matrícula visível: 2026001
- Nome visível: João Silva

### ✅ CT-002: Validação Nome
- Modal abre
- Nome deixado vazio
- Clique Salvar
- Alerta ou validação inline aparece
- Modal permanece aberta (não salvou)

### ✅ CT-003: Validação Datas
- Demissão: 2026-06-01
- Admissão: 2026-07-19
- Erro aparecer (demissão < admissão)

### ✅ CT-004: Matrícula Única
- Matrícula 2026001 já existe
- Tentar inserir novamente
- Erro: "Matrícula já cadastrada"

### ✅ CT-005: Editar
- Clique "Editar" em uma linha
- Modal abre com dados preenchidos
- Mude cargo: "Pedreiro" → "Encarregado"
- Clique Salvar
- Tabela atualiza com novo cargo

### ✅ CT-006: Detalhes
- Clique "Detalhes"
- Modal abre (read-only)
- Todos os 20 campos visíveis

### ✅ CT-007: Remover
- Clique "Remover"
- Diálogo confirma
- Colaborador desaparece da lista

### ✅ CT-008: Busca por Nome
- Digite "João" no campo de busca
- Lista filtra em tempo real
- Apenas linhas com "João" aparecem

### ✅ CT-009: Filtro Empresa
- Dropdown "Empresa"
- Selecione "Cesbe S.A."
- Lista mostra apenas Cesbe

### ✅ CT-010: Filtro Situação
- Dropdown "Situação"
- Selecione "Ativo"
- Lista mostra apenas ativos (badge verde)

### ✅ CT-011: Filtro Frente
- Dropdown "Frente"
- Selecione "Fundações"
- Lista filtra por frente

### ✅ CT-012: Ordenação
- Dropdown "Ordenar por"
- Escolha "Nome (Z-A)"
- Lista inverte ordem alfabética

### ✅ CT-013: Filtros Combinados
- Empresa: Cesbe
- Frente: Fundações
- Situação: Ativo
- Lista mostra apenas que atendem TODOS os critérios (AND)

### ✅ CT-014: Estatísticas
- Seção "Estatísticas" visível
- Cards com: Total, Ativos, Inativos, MOD, MOI, Terceiros
- Números fazem sentido (ex: Ativos ≤ Total)

### ✅ CT-015: Navegação Abas
- Novo colaborador → Aba 1 (Pessoal)
- Clique Aba 2 (Temporal) → mude data_admissao
- Clique Aba 3 (Operacional) → mude situacao
- Volte para Aba 1 → dados da Aba 1 ainda estão lá (preservados)

### ✅ CT-016: Responsividade
- Desktop (1920x1080) → tabela ok
- Tablet (768x1024) → modal redimensionada
- Mobile (375x667) → tudo em coluna, scrollável

### ✅ CT-017: Tema Claro/Escuro
- Cores funcionam no tema do SO
- Contraste legível
- Badges e ícones visíveis em ambos os temas

### ✅ CT-018: Integração Efetivo
- Novo colaborador criado
- Abra módulo "Efetivo" (presença)
- Novo colab aparece na lista de presença
- Marcar presença funciona

---

## 📞 Suporte

- **Documentação completa:** `README.md`
- **Guia rápido:** `GUIA-RAPIDO.md`
- **Documentação técnica:** `GUIA-DESENVOLVEDOR.md`
- **Testes detalhados:** `docs/TESTES-E2E.md`
- **API Reference:** `docs/API-COLABORADOR.md`

---

**Boa sorte! 🎉**

Data: 2026-07-19 | Versão: 1.0 | Fase: 5 (Testes)
