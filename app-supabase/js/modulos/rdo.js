// Buildly — módulo RDO (Diário de Obras), editor de um RDO específico.
// Persiste no Supabase: rdo, rdo_clima, rdo_atividade, rdo_maquina,
// rdo_ocorrencia, rdo_parecer_juridico.

const RDO_PERIODOS = [
  { chave: "madrugada", rotulo: "Madrugada", faixa: "00h00-06h59" },
  { chave: "manha", rotulo: "Manhã", faixa: "07h00-12h00" },
  { chave: "tarde", rotulo: "Tarde", faixa: "13h00-17h00" },
  { chave: "noite", rotulo: "Noite", faixa: "17h00-23h59" },
];

const RDO_CONDICOES_CLIMA = ["Limpo", "Nublado", "Chuvoso", "Encoberto"];

const RDO_ABAS = [
  { chave: "clima", rotulo: "Clima" },
  { chave: "atividades", rotulo: "Atividades" },
  { chave: "maquinas", rotulo: "Máquinas" },
  { chave: "ocorrencias", rotulo: "Ocorrências" },
  { chave: "observacoes", rotulo: "Observações" },
  { chave: "parecer", rotulo: "Parecer Jurídico" },
];

const RDO_STATUS_ROTULO = {
  rascunho: "Rascunho",
  em_aprovacao: "Em Aprovação",
  aprovado: "Aprovado",
  rejeitado: "Rejeitado",
};

async function carregarOuCriarRdo(obra, rdoId) {
  let rdo = null;

  if (rdoId) {
    const { data } = await db.from("rdo").select("*").eq("id", rdoId).maybeSingle();
    rdo = data;
  }

  if (!rdo) {
    const hoje = new Date().toISOString().slice(0, 10);
    const { data: existente } = await db
      .from("rdo").select("*").eq("obra_id", obra.id).eq("data", hoje).maybeSingle();
    rdo = existente;

    if (!rdo) {
      const { data: criado, error } = await db
        .from("rdo").insert({ obra_id: obra.id, data: hoje }).select().single();
      if (error) throw error;
      rdo = criado;
    }
  }

  const [climaResp, atividadesResp, maquinasResp, ocorrenciasResp, parecerResp] = await Promise.all([
    db.from("rdo_clima").select("*").eq("rdo_id", rdo.id),
    db.from("rdo_atividade").select("*").eq("rdo_id", rdo.id),
    db.from("rdo_maquina").select("*").eq("rdo_id", rdo.id),
    db.from("rdo_ocorrencia").select("*").eq("rdo_id", rdo.id),
    db.from("rdo_parecer_juridico").select("*").eq("rdo_id", rdo.id).maybeSingle(),
  ]);

  const clima = {};
  for (const p of RDO_PERIODOS) {
    const registro = (climaResp.data || []).find((c) => c.periodo === p.chave);
    clima[p.chave] = registro || { ativo: false, condicao: "Limpo", precipitacao_mm: 0 };
  }

  return {
    rdo,
    clima,
    atividades: atividadesResp.data || [],
    maquinas: maquinasResp.data || [],
    ocorrencias: ocorrenciasResp.data || [],
    parecer: parecerResp.data ? parecerResp.data.texto : "",
  };
}

async function renderModuloRDO(container, obra, rdoId) {
  container.innerHTML = `<p class="placeholder-modulo">Carregando RDO…</p>`;

  let estado;
  try {
    estado = await carregarOuCriarRdo(obra, rdoId);
  } catch (e) {
    console.error("Erro ao carregar RDO:", e);
    container.innerHTML = `<p class="login-erro">Erro ao carregar o RDO. Tente novamente.</p>`;
    return;
  }
  estado.abaAtiva = "clima";
  estado.salvando = false;

  function podeEditar() {
    return !estado.rdo.edicao_bloqueada;
  }

  async function salvarRdo(campos) {
    estado.salvando = true;
    const { error } = await db.from("rdo").update(campos).eq("id", estado.rdo.id);
    estado.salvando = false;
    if (error) {
      console.error("Erro ao salvar RDO:", error);
      return false;
    }
    Object.assign(estado.rdo, campos);
    return true;
  }

  async function salvarClima(periodo) {
    const c = estado.clima[periodo];
    const registro = {
      rdo_id: estado.rdo.id,
      periodo,
      ativo: c.ativo,
      condicao: c.condicao,
      precipitacao_mm: c.precipitacao_mm,
      origem: "manual",
    };
    const { data, error } = await db
      .from("rdo_clima")
      .upsert(registro, { onConflict: "rdo_id,periodo" })
      .select()
      .single();
    if (error) {
      console.error("Erro ao salvar clima:", error);
      return;
    }
    estado.clima[periodo] = data;
  }

  function render() {
    const rdo = estado.rdo;
    container.innerHTML = `
      <div class="rdo">
        <div class="rdo-header">
          <div>
            <button type="button" class="btn-texto" data-acao="voltar">← Voltar</button>
            <span class="rdo-data">RDO — ${formatarDataRdo(rdo.data)}</span>
            <span class="badge badge-${rdo.status}">${RDO_STATUS_ROTULO[rdo.status]}</span>
          </div>
          <div class="rdo-acoes">
            <button type="button" data-acao="enviar-aprovacao" class="btn-primario">
              ${rdo.status === "em_aprovacao" ? "Cancelar Aprovação" : "Enviar para Aprovação"}
            </button>
          </div>
        </div>

        <nav class="rdo-abas">
          ${RDO_ABAS.map(
            (aba) => `<button type="button" class="rdo-aba ${aba.chave === estado.abaAtiva ? "ativa" : ""}" data-aba="${aba.chave}">${aba.rotulo}</button>`
          ).join("")}
        </nav>

        <div class="rdo-conteudo-aba">${renderAba(estado.abaAtiva, rdo)}</div>
      </div>
    `;

    ligarEventos();
  }

  function renderAba(aba, rdo) {
    switch (aba) {
      case "clima":
        return renderAbaClima(rdo);
      case "atividades":
        return renderAbaLista(estado.atividades, "atividade", "Nenhuma atividade registrada.");
      case "maquinas":
        return renderAbaLista(estado.maquinas, "maquina", "Nenhuma máquina registrada.");
      case "ocorrencias":
        return renderAbaLista(estado.ocorrencias, "ocorrencia", "Nenhuma ocorrência registrada.");
      case "observacoes":
        return `
          <label class="campo">
            <span>Observações sobre as condições do dia (salva ao sair do campo)</span>
            <textarea data-campo="observacoes_condicoes" rows="6" ${podeEditar() ? "" : "disabled"}>${rdo.observacoes_condicoes || ""}</textarea>
          </label>`;
      case "parecer":
        return `
          <label class="campo">
            <span>Parecer Jurídico (salva ao sair do campo)</span>
            <textarea data-campo="parecer_juridico" rows="8" ${podeEditar() ? "" : "disabled"}>${estado.parecer || ""}</textarea>
          </label>`;
      default:
        return "";
    }
  }

  function renderAbaClima(rdo) {
    return `
      <p class="secao-descricao">Selecione os períodos ativos e a condição de cada um. As alterações são salvas automaticamente.</p>
      <div class="clima-grid">
        ${RDO_PERIODOS.map((p) => {
          const c = estado.clima[p.chave];
          return `
            <div class="clima-card ${c.ativo ? "" : "clima-card-inativo"}">
              <div class="clima-card-topo">
                <div>
                  <strong>${p.rotulo}</strong>
                  <span class="clima-faixa">${p.faixa}</span>
                </div>
                <label class="toggle">
                  <input type="checkbox" data-clima-ativo="${p.chave}" ${c.ativo ? "checked" : ""} ${podeEditar() ? "" : "disabled"}>
                  <span></span>
                </label>
              </div>
              <select data-clima-condicao="${p.chave}" ${c.ativo && podeEditar() ? "" : "disabled"}>
                ${RDO_CONDICOES_CLIMA.map((op) => `<option value="${op}" ${op === c.condicao ? "selected" : ""}>${op}</option>`).join("")}
              </select>
              <label class="campo-inline">
                <input type="number" step="0.1" min="0" data-clima-precipitacao="${p.chave}" value="${c.precipitacao_mm || 0}" ${c.ativo && podeEditar() ? "" : "disabled"}>
                <span>mm</span>
              </label>
            </div>`;
        }).join("")}
      </div>

      <p class="secao-descricao" style="margin-top:20px">Condições de Área</p>
      <div class="condicoes-area">
        ${["operavel", "inoperavel", "parcialmente_operavel"].map((valor) => `
          <label class="radio-inline">
            <input type="radio" name="condicao_area" value="${valor}" ${rdo.condicao_area === valor ? "checked" : ""} ${podeEditar() ? "" : "disabled"}>
            <span>${{ operavel: "Operável", inoperavel: "Inoperável", parcialmente_operavel: "Parcialmente operável" }[valor]}</span>
          </label>
        `).join("")}
      </div>`;
  }

  function renderAbaLista(itens, tipo, textoVazio) {
    const campoDescricao = { atividade: "descricao", maquina: "equipamento", ocorrencia: "descricao" }[tipo];
    return `
      <div class="lista-simples">
        ${itens.length === 0 ? `<p class="placeholder-modulo">${textoVazio}</p>` : itens.map((i) => `
          <div class="lista-item lista-item-flex">
            <span>${i[campoDescricao]}</span>
            ${podeEditar() ? `<button type="button" class="btn-texto" data-acao="remover-${tipo}" data-id="${i.id}">Remover</button>` : ""}
          </div>`).join("")}
        <button type="button" data-acao="adicionar-${tipo}" class="btn-secundario" ${podeEditar() ? "" : "disabled"}>+ Adicionar</button>
      </div>`;
  }

  function ligarEventos() {
    const botaoVoltar = container.querySelector('[data-acao="voltar"]');
    if (botaoVoltar) {
      botaoVoltar.addEventListener("click", () => {
        renderRdoDashboard(container, obra, {
          onNovoRdo: () => renderModuloRDO(container, obra),
          onAbrirRdo: (id) => renderModuloRDO(container, obra, id),
        });
      });
    }

    container.querySelectorAll("[data-aba]").forEach((botao) => {
      botao.addEventListener("click", () => {
        estado.abaAtiva = botao.dataset.aba;
        render();
      });
    });

    container.querySelectorAll("[data-clima-ativo]").forEach((input) => {
      input.addEventListener("change", async () => {
        const p = input.dataset.climaAtivo;
        estado.clima[p].ativo = input.checked;
        await salvarClima(p);
        render();
      });
    });

    container.querySelectorAll("[data-clima-condicao]").forEach((select) => {
      select.addEventListener("change", () => {
        const p = select.dataset.climaCondicao;
        estado.clima[p].condicao = select.value;
        salvarClima(p);
      });
    });

    container.querySelectorAll("[data-clima-precipitacao]").forEach((input) => {
      input.addEventListener("change", () => {
        const p = input.dataset.climaPrecipitacao;
        estado.clima[p].precipitacao_mm = parseFloat(input.value) || 0;
        salvarClima(p);
      });
    });

    container.querySelectorAll('input[name="condicao_area"]').forEach((input) => {
      input.addEventListener("change", () => {
        salvarRdo({ condicao_area: input.value });
      });
    });

    const campoObservacoes = container.querySelector('[data-campo="observacoes_condicoes"]');
    if (campoObservacoes) {
      campoObservacoes.addEventListener("blur", () => {
        salvarRdo({ observacoes_condicoes: campoObservacoes.value });
      });
    }

    const campoParecer = container.querySelector('[data-campo="parecer_juridico"]');
    if (campoParecer) {
      campoParecer.addEventListener("blur", async () => {
        estado.parecer = campoParecer.value;
        const { error } = await db
          .from("rdo_parecer_juridico")
          .upsert({ rdo_id: estado.rdo.id, texto: estado.parecer }, { onConflict: "rdo_id" });
        if (error) console.error("Erro ao salvar parecer:", error);
      });
    }

    const botaoAprovacao = container.querySelector('[data-acao="enviar-aprovacao"]');
    if (botaoAprovacao) {
      botaoAprovacao.addEventListener("click", async () => {
        const emAprovacao = estado.rdo.status === "em_aprovacao";
        const ok = await salvarRdo(
          emAprovacao
            ? { status: "rascunho", edicao_bloqueada: false }
            : { status: "em_aprovacao", edicao_bloqueada: true }
        );
        if (ok) render();
      });
    }

    const tabelasPorTipo = {
      atividade: { tabela: "rdo_atividade", lista: "atividades", campo: "descricao", pergunta: "Descrição da atividade:" },
      maquina: { tabela: "rdo_maquina", lista: "maquinas", campo: "equipamento", pergunta: "Equipamento:" },
      ocorrencia: { tabela: "rdo_ocorrencia", lista: "ocorrencias", campo: "descricao", pergunta: "Descrição da ocorrência:" },
    };

    for (const [tipo, cfg] of Object.entries(tabelasPorTipo)) {
      const botaoAdd = container.querySelector(`[data-acao="adicionar-${tipo}"]`);
      if (botaoAdd) {
        botaoAdd.addEventListener("click", async () => {
          const valor = window.prompt(cfg.pergunta);
          if (!valor) return;
          const { data, error } = await db
            .from(cfg.tabela)
            .insert({ rdo_id: estado.rdo.id, [cfg.campo]: valor })
            .select()
            .single();
          if (error) {
            console.error(`Erro ao adicionar ${tipo}:`, error);
            return;
          }
          estado[cfg.lista].push(data);
          render();
        });
      }

      container.querySelectorAll(`[data-acao="remover-${tipo}"]`).forEach((botao) => {
        botao.addEventListener("click", async () => {
          const id = botao.dataset.id;
          const { error } = await db.from(cfg.tabela).delete().eq("id", id);
          if (error) {
            console.error(`Erro ao remover ${tipo}:`, error);
            return;
          }
          estado[cfg.lista] = estado[cfg.lista].filter((i) => i.id !== id);
          render();
        });
      });
    }
  }

  function formatarDataRdo(iso) {
    const [ano, mes, dia] = iso.split("-");
    return `${dia}/${mes}/${ano}`;
  }

  render();
}
