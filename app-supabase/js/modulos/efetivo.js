// Buildly — módulo Efetivo (presença diária por obra).
// Usa o cadastro do módulo Gestão de Equipes (tabela colaborador); marcar a
// caixa cria o registro em efetivo_registro, desmarcar remove.

async function renderModuloEfetivo(container, obra, dataIso) {
  const data = dataIso || new Date().toISOString().slice(0, 10);
  container.innerHTML = `<p class="placeholder-modulo">Carregando efetivo…</p>`;

  const [colabResp, registrosResp] = await Promise.all([
    db.from("colaborador").select("*").order("nome"),
    db.from("efetivo_registro").select("colaborador_id").eq("obra_id", obra.id).eq("data", data),
  ]);

  if (colabResp.error || registrosResp.error) {
    console.error("Erro ao carregar efetivo:", colabResp.error || registrosResp.error);
    container.innerHTML = `<p class="login-erro">Erro ao carregar o efetivo. Tente novamente.</p>`;
    return;
  }

  const colaboradores = colabResp.data;
  const presentes = new Set(registrosResp.data.map((r) => r.colaborador_id));

  container.innerHTML = `
    <div class="efetivo">
      <div class="efetivo-topo">
        <label class="campo-inline">
          <span>Data:</span>
          <input type="date" id="efetivo-data" value="${data}">
        </label>
        <span class="badge">${presentes.size} presente${presentes.size === 1 ? "" : "s"} de ${colaboradores.length}</span>
      </div>

      <p class="secao-descricao">Marque quem está presente na obra nesta data. As alterações são salvas automaticamente.</p>

      <div class="lista-simples">
        ${colaboradores.length === 0
          ? `<p class="placeholder-modulo">Nenhum colaborador cadastrado — cadastre primeiro em Gestão de Equipes.</p>`
          : colaboradores.map((c) => `
          <label class="lista-item lista-item-flex efetivo-item">
            <div>
              <strong>${c.nome}</strong>
              <span class="texto-suave"> — ${c.empresa || ""}${c.funcao ? " · " + c.funcao : ""}</span>
            </div>
            <input type="checkbox" data-colaborador="${c.id}" ${presentes.has(c.id) ? "checked" : ""}>
          </label>`).join("")}
      </div>
    </div>
  `;

  container.querySelector("#efetivo-data").addEventListener("change", (evento) => {
    renderModuloEfetivo(container, obra, evento.target.value);
  });

  container.querySelectorAll("[data-colaborador]").forEach((checkbox) => {
    checkbox.addEventListener("change", async () => {
      const colaboradorId = checkbox.dataset.colaborador;

      if (checkbox.checked) {
        const { error } = await db.from("efetivo_registro").upsert(
          { obra_id: obra.id, colaborador_id: colaboradorId, data, presente: true },
          { onConflict: "obra_id,colaborador_id,data" }
        );
        if (error) {
          console.error("Erro ao marcar presença:", error);
          checkbox.checked = false;
          return;
        }
      } else {
        const { error } = await db
          .from("efetivo_registro")
          .delete()
          .eq("obra_id", obra.id)
          .eq("colaborador_id", colaboradorId)
          .eq("data", data);
        if (error) {
          console.error("Erro ao desmarcar presença:", error);
          checkbox.checked = true;
          return;
        }
      }

      renderModuloEfetivo(container, obra, data);
    });
  });
}
