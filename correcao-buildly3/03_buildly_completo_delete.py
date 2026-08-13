import pathlib

p = pathlib.Path("buildly-completo.html")
content = p.read_text(encoding="utf-8")

# Edit 1: pautaRemoverAssunto -> também apaga na planilha
old1 = """  pautaS.set('assuntos', pautaAssuntos);
  pautaRenderListar();
  pautaNotify('Removido', 'var(--red)');
}

function pautaLimparAssuntos() {"""

new1 = """  pautaS.set('assuntos', pautaAssuntos);
  pautaRenderListar();
  pautaNotify('Removido', 'var(--red)');

  // Apaga de verdade na planilha — sem isto, a linha continuava lá e a
  // próxima busca da planilha trazia o assunto de volta como se fosse novo.
  fetch(APPS_SCRIPT_URL, {
    method: 'POST',
    body: JSON.stringify({ path: 'pauta', action: 'remover', id })
  }).catch(e => console.warn('Pauta: não foi possível remover na planilha:', e.message));
}

function pautaLimparAssuntos() {"""

assert content.count(old1) == 1, f"edit1: esperava 1 ocorrência, achei {content.count(old1)}"
content = content.replace(old1, new1)

# Edit 2: sincronizarComGoogleSheets (pauta) -> corrige chave duplicada 'path' e envia id
old2 = """          body: JSON.stringify({
            path: 'pauta',
            action: 'criar',
            path: 'pauta',
            assunto: assunto.assunto,
            descricao: assunto.desc,
            criador: assunto.criador,"""

new2 = """          body: JSON.stringify({
            path: 'pauta',
            action: 'criar',
            id: assunto.id,
            assunto: assunto.assunto,
            descricao: assunto.desc,
            criador: assunto.criador,"""

assert content.count(old2) == 1, f"edit2: esperava 1 ocorrência, achei {content.count(old2)}"
content = content.replace(old2, new2)

# Edit 3: sincronizarComGoogleSheets (checkin) -> envia id
old3 = """          body: JSON.stringify({
            path: 'checkin',
            action: 'salvar',
            assunto: assunto.assunto,
            descricao: assunto.desc,
            criador: assunto.criador,"""

new3 = """          body: JSON.stringify({
            path: 'checkin',
            action: 'salvar',
            id: assunto.id,
            assunto: assunto.assunto,
            descricao: assunto.desc,
            criador: assunto.criador,"""

assert content.count(old3) == 1, f"edit3: esperava 1 ocorrência, achei {content.count(old3)}"
content = content.replace(old3, new3)

# Edit 4: checkinRemoverAssunto -> tombstone + apaga de verdade na planilha
old4 = """  checkinS.set('assuntos', checkinAssuntos);
  checkinRenderCadastro();
  checkinRenderKanban();
  checkinAtualizarContadores();
  checkinNotify('Removido', 'var(--red)');
}

function checkinSalvarReuniao() {"""

new4 = """  checkinS.set('assuntos', checkinAssuntos);

  // Lembra que este ID foi removido manualmente, para a sincronização com a
  // Pauta e a busca na planilha não reimportá-lo automaticamente depois.
  let idsRemovidos = [];
  try { idsRemovidos = JSON.parse(localStorage.getItem('chk_removidos') || '[]'); } catch { idsRemovidos = []; }
  if (!idsRemovidos.map(String).includes(String(id))) idsRemovidos.push(id);
  localStorage.setItem('chk_removidos', JSON.stringify(idsRemovidos));

  checkinRenderCadastro();
  checkinRenderKanban();
  checkinAtualizarContadores();
  checkinNotify('Removido', 'var(--red)');

  // Apaga de verdade na planilha — sem isto, a linha continuava lá e a
  // próxima busca da planilha trazia o assunto de volta como se fosse novo.
  fetch(APPS_SCRIPT_URL, {
    method: 'POST',
    body: JSON.stringify({ path: 'checkin', action: 'remover', id })
  }).catch(e => console.warn('Check-in: não foi possível remover na planilha:', e.message));
}

function checkinSalvarReuniao() {"""

assert content.count(old4) == 1, f"edit4: esperava 1 ocorrência, achei {content.count(old4)}"
content = content.replace(old4, new4)

p.write_text(content, encoding="utf-8")
print("buildly-completo.html atualizado com sucesso.")
