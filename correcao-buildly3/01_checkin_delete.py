import pathlib

p = pathlib.Path("Check-in.html")
content = p.read_text(encoding="utf-8")

old = """  let idsRemovidos = [];
  try { idsRemovidos = JSON.parse(localStorage.getItem('chk_removidos') || '[]'); } catch { idsRemovidos = []; }
  if (!idsRemovidos.map(String).includes(String(id))) idsRemovidos.push(id);
  localStorage.setItem('chk_removidos', JSON.stringify(idsRemovidos));

  renderCadastro();renderKanbanCheckin();atualizarContadores();
  notify('Removido','var(--red)');
}"""

new = """  let idsRemovidos = [];
  try { idsRemovidos = JSON.parse(localStorage.getItem('chk_removidos') || '[]'); } catch { idsRemovidos = []; }
  if (!idsRemovidos.map(String).includes(String(id))) idsRemovidos.push(id);
  localStorage.setItem('chk_removidos', JSON.stringify(idsRemovidos));

  if (APPS_SCRIPT_URL_PAUTA) {
    fetch(APPS_SCRIPT_URL_PAUTA, {
      method: 'POST',
      body: JSON.stringify({ path: 'checkin', action: 'remover', id })
    }).catch(e => console.warn('Check-in: não foi possível remover na planilha:', e.message));
  }

  renderCadastro();renderKanbanCheckin();atualizarContadores();
  notify('Removido','var(--red)');
}"""

assert content.count(old) == 1, f"esperava 1 ocorrência, achei {content.count(old)}"
content = content.replace(old, new)
p.write_text(content, encoding="utf-8")
print("Check-in.html atualizado com sucesso.")
