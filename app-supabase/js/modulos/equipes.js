// Buildly — módulo Gestão de Equipes (cadastro de colaboradores com 20 campos operacionais)
// O cadastro é global (não por obra); a presença por obra/dia fica no módulo Efetivo.

async function renderModuloEquipes(container) {
  container.innerHTML = `<p class="placeholder-modulo">Carregando equipe…</p>`;

  const { data: colaboradores, error } = await db
    .from("colaborador")
    .select("*")
    .order("nome");

  if (error) {
    console.error("Erro ao carregar colaboradores:", error);
    container.innerHTML = `<p class="login-erro">Erro ao carregar a equipe. Tente novamente.</p>`;
    return;
  }

  // Carregar lista de empresas únicas para filtro
  const empresas = [...new Set(colaboradores.map(c => c.empresa).filter(Boolean))];
  const frentes = [...new Set(colaboradores.map(c => c.frente_servico).filter(Boolean))];

  // Calcular estatísticas
  const stats = {
    total: colaboradores.length,
    ativos: colaboradores.filter(c => c.situacao === 'ativo').length,
    inativos: colaboradores.filter(c => c.situacao === 'inativo').length,
    mod: colaboradores.filter(c => c.tipo_mao_obra === 'mod').length,
    moi: colaboradores.filter(c => c.tipo_mao_obra === 'moi').length,
    terceiros: colaboradores.filter(c => c.tipo_mao_obra === 'terceirizado').length
  };

  container.innerHTML = `
    <div class="equipes">
      <div class="equipes-header">
        <h2>Gestão de Equipes</h2>
        <button type="button" class="btn-primario" id="btn-novo-colaborador">+ Novo Colaborador</button>
      </div>

      <div id="modal-colaborador" class="modal" style="display:none;">
        <div class="modal-content">
          <div class="modal-header">
            <h3 id="modal-titulo">Novo Colaborador</h3>
            <button type="button" class="modal-close" id="btn-fechar-modal">&times;</button>
          </div>

          <div class="modal-body">
            <form id="form-colaborador">
              <!-- Abas de Navegação -->
              <div class="tabs">
                <button type="button" class="tab-btn active" data-tab="tab-pessoal">📋 Dados Pessoais</button>
                <button type="button" class="tab-btn" data-tab="tab-temporal">📅 Temporal</button>
                <button type="button" class="tab-btn" data-tab="tab-operacional">🏗️ Operacional</button>
              </div>

              <!-- TAB 1: Dados Pessoais -->
              <div class="tab-content active" id="tab-pessoal">
                <div class="form-group">
                  <label for="col-matricula">Matrícula</label>
                  <input type="number" id="col-matricula" class="form-control" />
                </div>

                <div class="form-group">
                  <label for="col-nome">
                    Nome <span class="required">*</span>
                  </label>
                  <input type="text" id="col-nome" class="form-control" required />
                </div>

                <div class="form-group">
                  <label for="col-sexo">Sexo</label>
                  <select id="col-sexo" class="form-control">
                    <option value="">-- Selecione --</option>
                    <option value="masculino">Masculino</option>
                    <option value="feminino">Feminino</option>
                    <option value="não_informado">Não informado</option>
                  </select>
                </div>

                <div class="form-group">
                  <label for="col-cidade">Cidade</label>
                  <input type="text" id="col-cidade" class="form-control" />
                </div>

                <div class="form-group">
                  <label for="col-estado">Estado/UF</label>
                  <select id="col-estado" class="form-control">
                    <option value="">-- Selecione --</option>
                    <option value="SP">São Paulo</option>
                    <option value="RJ">Rio de Janeiro</option>
                    <option value="MG">Minas Gerais</option>
                    <option value="BA">Bahia</option>
                    <option value="PR">Paraná</option>
                    <option value="SC">Santa Catarina</option>
                    <option value="RS">Rio Grande do Sul</option>
                    <!-- ... mais estados ... -->
                  </select>
                </div>

                <div class="form-group">
                  <label for="col-cargo">Cargo</label>
                  <input type="text" id="col-cargo" class="form-control" placeholder="Ex: Pedreiro, Encarregado" />
                </div>

                <div class="form-group">
                  <label for="col-empresa">Empresa</label>
                  <input type="text" id="col-empresa" class="form-control" value="Cesbe S.A." />
                </div>
              </div>

              <!-- TAB 2: Temporal -->
              <div class="tab-content" id="tab-temporal">
                <div class="form-group">
                  <label for="col-admissao">Admissão</label>
                  <input type="date" id="col-admissao" class="form-control" />
                </div>

                <div class="form-group">
                  <label for="col-demissao">Demissão</label>
                  <input type="date" id="col-demissao" class="form-control" />
                </div>

                <div class="form-group">
                  <label for="col-termino-exp1">Término 1ª Experiência</label>
                  <input type="date" id="col-termino-exp1" class="form-control" />
                </div>

                <div class="form-group">
                  <label for="col-termino-exp2">Término 2ª Experiência</label>
                  <input type="date" id="col-termino-exp2" class="form-control" />
                </div>

                <div class="form-group">
                  <label for="col-estabilidade">Estabilidade</label>
                  <input type="text" id="col-estabilidade" class="form-control" placeholder="Ex: até 30/06/2026" />
                </div>
              </div>

              <!-- TAB 3: Operacional -->
              <div class="tab-content" id="tab-operacional">
                <div class="form-group">
                  <label for="col-situacao">Situação</label>
                  <select id="col-situacao" class="form-control">
                    <option value="ativo">Ativo</option>
                    <option value="inativo">Inativo</option>
                    <option value="afastado">Afastado</option>
                    <option value="licença">Licença</option>
                  </select>
                </div>

                <div class="form-group">
                  <label for="col-mao-obra">Mão de Obra</label>
                  <select id="col-mao-obra" class="form-control">
                    <option value="">-- Selecione --</option>
                    <option value="moi">MOI (Mão de obra indireta)</option>
                    <option value="mod">MOD (Mão de obra direta)</option>
                    <option value="terceirizado">Terceirizado</option>
                  </select>
                </div>

                <div class="form-group">
                  <label for="col-frente">Frente de Serviço</label>
                  <input type="text" id="col-frente" class="form-control" />
                </div>

                <div class="form-group">
                  <label for="col-local-registro">Local de Registro</label>
                  <input type="text" id="col-local-registro" class="form-control" />
                </div>

                <div class="form-group">
                  <label for="col-mobilizacao">Status Mobilização</label>
                  <select id="col-mobilizacao" class="form-control">
                    <option value="não_iniciado">Não iniciado</option>
                    <option value="em_progresso">Em progresso</option>
                    <option value="concluído">Concluído</option>
                    <option value="cancelado">Cancelado</option>
                  </select>
                </div>

                <div class="form-group">
                  <label for="col-alojamento">Status Alojamento</label>
                  <select id="col-alojamento" class="form-control">
                    <option value="não_necessário">Não necessário</option>
                    <option value="necessário">Necessário</option>
                    <option value="fornecido">Fornecido</option>
                    <option value="recusado">Recusado</option>
                  </select>
                </div>
              </div>
            </form>
          </div>

          <div class="modal-footer">
            <button type="button" class="btn-secondary" id="btn-cancelar">Cancelar</button>
            <button type="button" class="btn-primary" id="btn-salvar">Salvar</button>
          </div>
        </div>
      </div>

      <!-- Filtros e Busca -->
      <div class="filtros-equipe" style="margin-top:20px; padding:15px; background:var(--cor-superficie-alt); border-radius:6px;">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-bottom: 15px;">
          <div class="form-group">
            <label for="filtro-busca">🔍 Buscar por Nome</label>
            <input type="text" id="filtro-busca" class="form-control" placeholder="Digite o nome..." />
          </div>

          <div class="form-group">
            <label for="filtro-empresa">Empresa</label>
            <select id="filtro-empresa" class="form-control">
              <option value="">-- Todas --</option>
              ${empresas.map(e => `<option value="${e}">${e}</option>`).join('')}
            </select>
          </div>

          <div class="form-group">
            <label for="filtro-situacao">Situação</label>
            <select id="filtro-situacao" class="form-control">
              <option value="">-- Todas --</option>
              <option value="ativo">Ativo</option>
              <option value="inativo">Inativo</option>
              <option value="afastado">Afastado</option>
              <option value="licença">Licença</option>
            </select>
          </div>

          <div class="form-group">
            <label for="filtro-frente">Frente de Serviço</label>
            <select id="filtro-frente" class="form-control">
              <option value="">-- Todas --</option>
              ${frentes.map(f => `<option value="${f}">${f}</option>`).join('')}
            </select>
          </div>

          <div class="form-group">
            <label for="filtro-ordenacao">Ordenar por</label>
            <select id="filtro-ordenacao" class="form-control">
              <option value="nome">Nome (A-Z)</option>
              <option value="nome-desc">Nome (Z-A)</option>
              <option value="empresa">Empresa</option>
              <option value="cargo">Cargo</option>
              <option value="admissao">Data Admissão</option>
            </select>
          </div>

          <div style="display: flex; align-items: flex-end;">
            <button type="button" class="btn-secundario" id="btn-limpar-filtros" style="width:100%;">🔄 Limpar Filtros</button>
          </div>
        </div>

        <!-- Estatísticas -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 10px; font-size: 0.9em;">
          <div style="background: var(--cor-fundo); padding: 10px; border-radius: 4px; text-align: center;">
            <div style="font-size: 1.5em; font-weight: bold; color: var(--cor-primaria);">${stats.total}</div>
            <div style="color: var(--cor-texto-suave);">Total</div>
          </div>
          <div style="background: var(--cor-fundo); padding: 10px; border-radius: 4px; text-align: center;">
            <div style="font-size: 1.5em; font-weight: bold; color: #8fbf9f;">${stats.ativos}</div>
            <div style="color: var(--cor-texto-suave);">Ativos</div>
          </div>
          <div style="background: var(--cor-fundo); padding: 10px; border-radius: 4px; text-align: center;">
            <div style="font-size: 1.5em; font-weight: bold; color: #d4a574;">${stats.inativos}</div>
            <div style="color: var(--cor-texto-suave);">Inativos</div>
          </div>
          <div style="background: var(--cor-fundo); padding: 10px; border-radius: 4px; text-align: center;">
            <div style="font-size: 1.5em; font-weight: bold; color: #8fbf9f;">${stats.mod}</div>
            <div style="color: var(--cor-texto-suave);">MOD</div>
          </div>
          <div style="background: var(--cor-fundo); padding: 10px; border-radius: 4px; text-align: center;">
            <div style="font-size: 1.5em; font-weight: bold; color: #8fbf9f;">${stats.moi}</div>
            <div style="color: var(--cor-texto-suave);">MOI</div>
          </div>
          <div style="background: var(--cor-fundo); padding: 10px; border-radius: 4px; text-align: center;">
            <div style="font-size: 1.5em; font-weight: bold; color: #8fbf9f;">${stats.terceiros}</div>
            <div style="color: var(--cor-texto-suave);">Terceiros</div>
          </div>
        </div>
      </div>

      <!-- Lista de Colaboradores -->
      <div class="lista-colaboradores" style="margin-top:30px" id="lista-colaboradores-container">
        ${colaboradores.length === 0
          ? `<p class="placeholder-modulo">Nenhum colaborador cadastrado.</p>`
          : `
            <table class="tabela-colaboradores">
              <thead>
                <tr>
                  <th>Matrícula</th>
                  <th>Nome</th>
                  <th>Empresa</th>
                  <th>Cargo</th>
                  <th>Frente</th>
                  <th>Situação</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                ${colaboradores.map((c) => `
                  <tr>
                    <td>${c.matricula || '—'}</td>
                    <td><strong>${c.nome}</strong></td>
                    <td>${c.empresa || '—'}</td>
                    <td>${c.cargo || '—'}</td>
                    <td>${c.frente_servico || '—'}</td>
                    <td><span class="badge badge-${c.situacao === 'ativo' ? 'success' : 'warning'}">${c.situacao || '—'}</span></td>
                    <td>
                      <button type="button" class="btn-sm btn-info" data-acao="editar" data-id="${c.id}">Editar</button>
                      <button type="button" class="btn-sm btn-secondary" data-acao="detalhes" data-id="${c.id}">Detalhes</button>
                      <button type="button" class="btn-sm btn-danger" data-acao="remover" data-id="${c.id}">Remover</button>
                    </td>
                  </tr>
                \`).join('')}
              </tbody>
            </table>
          `}
      </div>
    </div>
  `;

  // ========== SETUP DE EVENTOS ==========

  // Abrir modal de novo colaborador
  container.querySelector("#btn-novo-colaborador").addEventListener("click", () => {
    limparFormulario();
    document.getElementById("modal-titulo").textContent = "Novo Colaborador";
    document.getElementById("form-colaborador").dataset.colaboradorId = "";
    document.getElementById("modal-colaborador").style.display = "flex";
  });

  // Fechar modal
  container.querySelector("#btn-fechar-modal").addEventListener("click", () => {
    document.getElementById("modal-colaborador").style.display = "none";
  });

  container.querySelector("#btn-cancelar").addEventListener("click", () => {
    document.getElementById("modal-colaborador").style.display = "none";
  });

  // Navegação entre abas
  container.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const tabName = e.target.dataset.tab;

      container.querySelectorAll(".tab-content").forEach((tab) => {
        tab.classList.remove("active");
      });
      container.querySelectorAll(".tab-btn").forEach((b) => {
        b.classList.remove("active");
      });

      document.getElementById(tabName).classList.add("active");
      e.target.classList.add("active");
    });
  });

  // Salvar colaborador (INSERT ou UPDATE)
  container.querySelector("#btn-salvar").addEventListener("click", async () => {
    await salvarColaborador();
  });

  // Editar colaborador
  container.querySelectorAll('[data-acao="editar"]').forEach((btn) => {
    btn.addEventListener("click", async () => {
      await abrirFormularioEdicao(btn.dataset.id);
    });
  });

  // Ver detalhes
  container.querySelectorAll('[data-acao="detalhes"]').forEach((btn) => {
    btn.addEventListener("click", async () => {
      await mostrarDetalhes(btn.dataset.id);
    });
  });

  // Remover colaborador
  container.querySelectorAll('[data-acao="remover"]').forEach((btn) => {
    btn.addEventListener("click", async () => {
      await removerColaborador(btn.dataset.id);
    });
  });

  // ========== FILTROS E BUSCA ==========

  const filtrosBusca = {
    busca: "",
    empresa: "",
    situacao: "",
    frente: "",
    ordenacao: "nome"
  };

  const filtrarERefazerlista = () => {
    let resultados = [...colaboradores];

    // Filtro de busca por nome
    if (filtrosBusca.busca) {
      resultados = resultados.filter(c =>
        c.nome.toLowerCase().includes(filtrosBusca.busca.toLowerCase())
      );
    }

    // Filtro por empresa
    if (filtrosBusca.empresa) {
      resultados = resultados.filter(c => c.empresa === filtrosBusca.empresa);
    }

    // Filtro por situação
    if (filtrosBusca.situacao) {
      resultados = resultados.filter(c => c.situacao === filtrosBusca.situacao);
    }

    // Filtro por frente
    if (filtrosBusca.frente) {
      resultados = resultados.filter(c => c.frente_servico === filtrosBusca.frente);
    }

    // Ordenação
    switch (filtrosBusca.ordenacao) {
      case "nome-desc":
        resultados.sort((a, b) => b.nome.localeCompare(a.nome));
        break;
      case "empresa":
        resultados.sort((a, b) => (a.empresa || "").localeCompare(b.empresa || ""));
        break;
      case "cargo":
        resultados.sort((a, b) => (a.cargo || "").localeCompare(b.cargo || ""));
        break;
      case "admissao":
        resultados.sort((a, b) => new Date(b.data_admissao || 0) - new Date(a.data_admissao || 0));
        break;
      default: // "nome"
        resultados.sort((a, b) => a.nome.localeCompare(b.nome));
    }

    // Re-renderizar tabela
    const listaContainer = container.querySelector("#lista-colaboradores-container");
    if (resultados.length === 0) {
      listaContainer.innerHTML = `<p class="placeholder-modulo">Nenhum colaborador encontrado com esses filtros.</p>`;
    } else {
      listaContainer.innerHTML = `
        <table class="tabela-colaboradores">
          <thead>
            <tr>
              <th>Matrícula</th>
              <th>Nome</th>
              <th>Empresa</th>
              <th>Cargo</th>
              <th>Frente</th>
              <th>Situação</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            ${resultados.map((c) => `
              <tr>
                <td>${c.matricula || '—'}</td>
                <td><strong>${c.nome}</strong></td>
                <td>${c.empresa || '—'}</td>
                <td>${c.cargo || '—'}</td>
                <td>${c.frente_servico || '—'}</td>
                <td><span class="badge badge-${c.situacao === 'ativo' ? 'success' : 'warning'}">${c.situacao || '—'}</span></td>
                <td>
                  <button type="button" class="btn-sm btn-info" data-acao="editar" data-id="${c.id}">Editar</button>
                  <button type="button" class="btn-sm btn-secondary" data-acao="detalhes" data-id="${c.id}">Detalhes</button>
                  <button type="button" class="btn-sm btn-danger" data-acao="remover" data-id="${c.id}">Remover</button>
                </td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      `;

      // Re-anexar handlers às novas linhas
      listaContainer.querySelectorAll('[data-acao="editar"]').forEach((btn) => {
        btn.addEventListener("click", async () => {
          await abrirFormularioEdicao(btn.dataset.id);
        });
      });

      listaContainer.querySelectorAll('[data-acao="detalhes"]').forEach((btn) => {
        btn.addEventListener("click", async () => {
          await mostrarDetalhes(btn.dataset.id);
        });
      });

      listaContainer.querySelectorAll('[data-acao="remover"]').forEach((btn) => {
        btn.addEventListener("click", async () => {
          await removerColaborador(btn.dataset.id);
        });
      });
    }
  };

  // Listeners para filtros
  container.querySelector("#filtro-busca").addEventListener("input", (e) => {
    filtrosBusca.busca = e.target.value;
    filtrarERefazerlista();
  });

  container.querySelector("#filtro-empresa").addEventListener("change", (e) => {
    filtrosBusca.empresa = e.target.value;
    filtrarERefazerlista();
  });

  container.querySelector("#filtro-situacao").addEventListener("change", (e) => {
    filtrosBusca.situacao = e.target.value;
    filtrarERefazerlista();
  });

  container.querySelector("#filtro-frente").addEventListener("change", (e) => {
    filtrosBusca.frente = e.target.value;
    filtrarERefazerlista();
  });

  container.querySelector("#filtro-ordenacao").addEventListener("change", (e) => {
    filtrosBusca.ordenacao = e.target.value;
    filtrarERefazerlista();
  });

  container.querySelector("#btn-limpar-filtros").addEventListener("click", () => {
    filtrosBusca.busca = "";
    filtrosBusca.empresa = "";
    filtrosBusca.situacao = "";
    filtrosBusca.frente = "";
    filtrosBusca.ordenacao = "nome";

    container.querySelector("#filtro-busca").value = "";
    container.querySelector("#filtro-empresa").value = "";
    container.querySelector("#filtro-situacao").value = "";
    container.querySelector("#filtro-frente").value = "";
    container.querySelector("#filtro-ordenacao").value = "nome";

    filtrarERefazerlista();
  });
}

// ========== FUNÇÕES AUXILIARES ==========

function limparFormulario() {
  document.getElementById("form-colaborador").reset();
  document.getElementById("col-empresa").value = "Cesbe S.A.";
  document.getElementById("col-situacao").value = "ativo";
  document.getElementById("col-mobilizacao").value = "não_iniciado";
  document.getElementById("col-alojamento").value = "não_necessário";
  document.getElementById("col-sexo").value = "não_informado";
}

async function salvarColaborador() {
  const form = document.getElementById("form-colaborador");

  // Coletar dados
  const formData = {
    matricula: parseInt(document.getElementById("col-matricula").value) || null,
    nome: document.getElementById("col-nome").value.trim(),
    sexo: document.getElementById("col-sexo").value || null,
    cidade: document.getElementById("col-cidade").value.trim() || null,
    estado: document.getElementById("col-estado").value || null,
    cargo: document.getElementById("col-cargo").value.trim() || null,
    empresa: document.getElementById("col-empresa").value.trim() || null,

    data_admissao: document.getElementById("col-admissao").value || null,
    data_demissao: document.getElementById("col-demissao").value || null,
    data_termino_exp1: document.getElementById("col-termino-exp1").value || null,
    data_termino_exp2: document.getElementById("col-termino-exp2").value || null,
    estabilidade: document.getElementById("col-estabilidade").value.trim() || null,

    situacao: document.getElementById("col-situacao").value || "ativo",
    tipo_mao_obra: document.getElementById("col-mao-obra").value || null,
    frente_servico: document.getElementById("col-frente").value.trim() || null,
    local_registro: document.getElementById("col-local-registro").value.trim() || null,
    status_mobilizacao: document.getElementById("col-mobilizacao").value || "não_iniciado",
    status_alojamento: document.getElementById("col-alojamento").value || "não_necessário"
  };

  // Validar campo obrigatório
  if (!formData.nome) {
    alert("Nome é obrigatório");
    return;
  }

  // Validar lógica de datas
  if (formData.data_admissao && formData.data_demissao) {
    if (new Date(formData.data_demissao) < new Date(formData.data_admissao)) {
      alert("Data de demissão não pode ser anterior à admissão");
      return;
    }
  }

  try {
    const colaboradorId = form.dataset.colaboradorId;

    if (colaboradorId) {
      // UPDATE
      const { error } = await db
        .from("colaborador")
        .update(formData)
        .eq("id", colaboradorId);

      if (error) throw error;
      alert("Colaborador atualizado com sucesso!");
    } else {
      // INSERT
      const { error } = await db
        .from("colaborador")
        .insert([formData]);

      if (error) throw error;
      alert("Colaborador criado com sucesso!");
    }

    document.getElementById("modal-colaborador").style.display = "none";
    limparFormulario();

    // Recarregar lista
    const container = document.querySelector(".equipes");
    renderModuloEquipes(container);
  } catch (error) {
    console.error("Erro ao salvar:", error);
    alert(`Erro: ${error.message}`);
  }
}

async function abrirFormularioEdicao(id) {
  try {
    const { data, error } = await db
      .from("colaborador")
      .select("*")
      .eq("id", id)
      .single();

    if (error) throw error;

    // Preencher formulário
    document.getElementById("col-matricula").value = data.matricula || "";
    document.getElementById("col-nome").value = data.nome || "";
    document.getElementById("col-sexo").value = data.sexo || "";
    document.getElementById("col-cidade").value = data.cidade || "";
    document.getElementById("col-estado").value = data.estado || "";
    document.getElementById("col-cargo").value = data.cargo || "";
    document.getElementById("col-empresa").value = data.empresa || "Cesbe S.A.";

    document.getElementById("col-admissao").value = data.data_admissao || "";
    document.getElementById("col-demissao").value = data.data_demissao || "";
    document.getElementById("col-termino-exp1").value = data.data_termino_exp1 || "";
    document.getElementById("col-termino-exp2").value = data.data_termino_exp2 || "";
    document.getElementById("col-estabilidade").value = data.estabilidade || "";

    document.getElementById("col-situacao").value = data.situacao || "ativo";
    document.getElementById("col-mao-obra").value = data.tipo_mao_obra || "";
    document.getElementById("col-frente").value = data.frente_servico || "";
    document.getElementById("col-local-registro").value = data.local_registro || "";
    document.getElementById("col-mobilizacao").value = data.status_mobilizacao || "não_iniciado";
    document.getElementById("col-alojamento").value = data.status_alojamento || "não_necessário";

    document.getElementById("form-colaborador").dataset.colaboradorId = id;
    document.getElementById("modal-titulo").textContent = `Editar - ${data.nome}`;
    document.getElementById("modal-colaborador").style.display = "flex";
  } catch (error) {
    console.error("Erro ao carregar colaborador:", error);
    alert(`Erro: ${error.message}`);
  }
}

async function mostrarDetalhes(id) {
  try {
    const { data, error } = await db
      .from("colaborador")
      .select("*")
      .eq("id", id)
      .single();

    if (error) throw error;

    const detalhes = `
      <h3>${data.nome}</h3>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
        <div>
          <p><strong>Matrícula:</strong> ${data.matricula || "—"}</p>
          <p><strong>Empresa:</strong> ${data.empresa || "—"}</p>
          <p><strong>Cargo:</strong> ${data.cargo || "—"}</p>
          <p><strong>Sexo:</strong> ${data.sexo || "—"}</p>
          <p><strong>Cidade:</strong> ${data.cidade || "—"}</p>
          <p><strong>Estado:</strong> ${data.estado || "—"}</p>
          <p><strong>Admissão:</strong> ${data.data_admissao || "—"}</p>
          <p><strong>Demissão:</strong> ${data.data_demissao || "—"}</p>
          <p><strong>Estabilidade:</strong> ${data.estabilidade || "—"}</p>
          <p><strong>Local de Registro:</strong> ${data.local_registro || "—"}</p>
        </div>
        <div>
          <p><strong>Situação:</strong> ${data.situacao || "—"}</p>
          <p><strong>Mão de Obra:</strong> ${data.tipo_mao_obra || "—"}</p>
          <p><strong>Frente:</strong> ${data.frente_servico || "—"}</p>
          <p><strong>Mobilização:</strong> ${data.status_mobilizacao || "—"}</p>
          <p><strong>Alojamento:</strong> ${data.status_alojamento || "—"}</p>
          <p><strong>Término 1ª Exp.:</strong> ${data.data_termino_exp1 || "—"}</p>
          <p><strong>Término 2ª Exp.:</strong> ${data.data_termino_exp2 || "—"}</p>
        </div>
      </div>
    `;

    alert(detalhes);
  } catch (error) {
    console.error("Erro ao buscar detalhes:", error);
    alert(`Erro: ${error.message}`);
  }
}

async function removerColaborador(id) {
  if (!confirm("Tem certeza que deseja remover este colaborador?")) return;

  try {
    const { error } = await db
      .from("colaborador")
      .delete()
      .eq("id", id);

    if (error) throw error;
    alert("Colaborador removido com sucesso!");

    const container = document.querySelector(".equipes");
    renderModuloEquipes(container);
  } catch (error) {
    console.error("Erro ao remover:", error);
    alert(`Erro: ${error.message}`);
  }
}
