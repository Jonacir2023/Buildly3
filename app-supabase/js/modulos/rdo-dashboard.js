// Buildly — dashboard/lista do módulo RDO
// Lê dados reais do Supabase (rdo, rdo_clima, efetivo_registro). Diferente do
// editor de um RDO específico (js/modulos/rdo.js), que ainda é mock.

const RDO_DASH_STATUS_ROTULO = {
  rascunho: "Em elaboração",
  em_aprovacao: "Pendente de aprovação",
  aprovado: "Aprovados",
  rejeitado: "Reprovados",
};

const RDO_DASH_CORES_CLIMA = {
  Limpo: "#c05f3c",
  Nublado: "#b8853a",
  Chuvoso: "#4d7c5f",
  Encoberto: "#7a7266",
};

function diasUteisEntre(inicio, fim) {
  if (!inicio) return 0;
  let count = 0;
  const cursor = new Date(inicio);
  const limite = new Date(fim);
  while (cursor <= limite) {
    const diaSemana = cursor.getDay();
    if (diaSemana !== 0 && diaSemana !== 6) count++;
    cursor.setDate(cursor.getDate() + 1);
  }
  return count;
}

function formatarDataCurta(iso) {
  const [, mes, dia] = iso.split("-");
  return `${dia}/${mes}`;
}

async function renderRdoDashboard(container, obra, { onNovoRdo, onAbrirRdo } = {}) {
  container.innerHTML = `<p class="placeholder-modulo">Carregando dashboard…</p>`;

  const hojeIso = new Date().toISOString().slice(0, 10);

  const [obraResp, rdosResp, climaResp, efetivoResp] = await Promise.all([
    db.from("obra").select("data_inicio, data_termino_prevista").eq("id", obra.id).maybeSingle(),
    db.from("rdo").select("id, data, status").eq("obra_id", obra.id).order("data", { ascending: false }),
    db
      .from("rdo_clima")
      .select("condicao, rdo!inner(obra_id)")
      .eq("ativo", true)
      .eq("rdo.obra_id", obra.id),
    db
      .from("efetivo_registro")
      .select("data, presente")
      .eq("obra_id", obra.id)
      .eq("presente", true)
      .order("data", { ascending: false })
      .limit(500),
  ]);

  const dadosObra = obraResp.data || {};
  const rdos = rdosResp.data || [];
  const climaRegistros = climaResp.data || [];
  const efetivoRegistros = efetivoResp.data || [];

  const contagemStatus = { rascunho: 0, em_aprovacao: 0, aprovado: 0, rejeitado: 0 };
  for (const r of rdos) {
    if (contagemStatus[r.status] !== undefined) contagemStatus[r.status]++;
  }

  const diasUteis = dadosObra.data_inicio ? diasUteisEntre(dadosObra.data_inicio, hojeIso) : 0;
  const diasComRdo = new Set(rdos.map((r) => r.data)).size;
  const diasSemRdo = Math.max(diasUteis - diasComRdo, 0);
  const cobertura = diasUteis > 0 ? Math.round((diasComRdo / diasUteis) * 100) : 0;

  const climaContagem = {};
  for (const c of climaRegistros) {
    climaContagem[c.condicao] = (climaContagem[c.condicao] || 0) + 1;
  }
  const climaTotal = Object.values(climaContagem).reduce((a, b) => a + b, 0);

  const efetivoPorDia = {};
  for (const e of efetivoRegistros) {
    efetivoPorDia[e.data] = (efetivoPorDia[e.data] || 0) + 1;
  }
  const ultimosDias = Object.keys(efetivoPorDia).sort().slice(-14);
  const maxEfetivo = Math.max(1, ...ultimosDias.map((d) => efetivoPorDia[d]));

  container.innerHTML = `
    <div class="rdo-dash">
      <div class="rdo-dash-topo">
        <button type="button" class="btn-primario" data-acao="novo-rdo">+ Novo RDO</button>
      </div>

      <div class="stat-grid">
        ${["rascunho", "em_aprovacao", "aprovado", "rejeitado"]
          .map(
            (chave) => `
          <div class="stat-card">
            <span class="stat-valor">${contagemStatus[chave]}</span>
            <span class="stat-rotulo">${RDO_DASH_STATUS_ROTULO[chave]}</span>
          </div>`
          )
          .join("")}
        <div class="stat-card">
          <span class="stat-valor">${rdos.length}</span>
          <span class="stat-rotulo">Total de RDOs</span>
        </div>
      </div>

      <div class="painel-grid">
        <div class="painel">
          <h3>Dados da Obra</h3>
          <dl class="painel-lista">
            <div><dt>Início da obra</dt><dd>${dadosObra.data_inicio ? formatarDataCurta(dadosObra.data_inicio) : "—"}</dd></div>
            <div><dt>Previsão de conclusão</dt><dd>${dadosObra.data_termino_prevista ? formatarDataCurta(dadosObra.data_termino_prevista) : "—"}</dd></div>
          </dl>
        </div>

        <div class="painel">
          <h3>Cobertura de RDOs</h3>
          <dl class="painel-lista">
            <div><dt>Dias úteis no período</dt><dd>${diasUteis}</dd></div>
            <div><dt>Dias sem RDO</dt><dd>${diasSemRdo}</dd></div>
            <div><dt>Cobertura</dt><dd>${cobertura}%</dd></div>
          </dl>
        </div>

        <div class="painel">
          <h3>Condições Climáticas</h3>
          ${
            climaTotal === 0
              ? `<p class="placeholder-modulo">Sem registros de clima ainda.</p>`
              : `
            <div class="clima-legenda">
              ${Object.entries(climaContagem)
                .map(
                  ([cond, qtd]) => `
                <div class="clima-legenda-item">
                  <span class="clima-dot" style="background:${RDO_DASH_CORES_CLIMA[cond] || "#999"}"></span>
                  ${cond} — ${Math.round((qtd / climaTotal) * 100)}%
                </div>`
                )
                .join("")}
            </div>`
          }
        </div>
      </div>

      <div class="painel">
        <h3>Histograma de Efetivo (últimos dias)</h3>
        ${
          ultimosDias.length === 0
            ? `<p class="placeholder-modulo">Sem registros de efetivo ainda.</p>`
            : `
          <div class="histograma">
            ${ultimosDias
              .map(
                (d) => `
              <div class="histograma-barra-wrap" title="${formatarDataCurta(d)}: ${efetivoPorDia[d]}">
                <div class="histograma-barra" style="height:${(efetivoPorDia[d] / maxEfetivo) * 100}%"></div>
                <span class="histograma-rotulo">${formatarDataCurta(d)}</span>
              </div>`
              )
              .join("")}
          </div>`
        }
      </div>

      <div class="painel">
        <h3>RDOs recentes</h3>
        ${
          rdos.length === 0
            ? `<p class="placeholder-modulo">Nenhum RDO lançado ainda para esta obra.</p>`
            : `
          <div class="lista-simples">
            ${rdos
              .slice(0, 10)
              .map(
                (r) => `
              <button type="button" class="lista-item lista-item-clicavel" data-acao="abrir-rdo" data-id="${r.id}">
                <span>${formatarDataCurta(r.data)}</span>
                <span class="badge badge-${r.status}">${RDO_DASH_STATUS_ROTULO[r.status] || r.status}</span>
              </button>`
              )
              .join("")}
          </div>`
        }
      </div>
    </div>
  `;

  const botaoNovo = container.querySelector('[data-acao="novo-rdo"]');
  if (botaoNovo && onNovoRdo) {
    botaoNovo.addEventListener("click", onNovoRdo);
  }

  container.querySelectorAll('[data-acao="abrir-rdo"]').forEach((botao) => {
    botao.addEventListener("click", () => {
      if (onAbrirRdo) onAbrirRdo(botao.dataset.id);
    });
  });
}
