import pathlib

p = pathlib.Path("pauta.html")
content = p.read_text(encoding="utf-8")

# Edit 1: removerAssunto -> também apaga na planilha
old1 = """  S.set('assuntos', assuntos);
  renderListar();
  notify('Removido','var(--red)');
}

function limparAssuntos(){"""

new1 = """  S.set('assuntos', assuntos);
  renderListar();
  notify('Removido','var(--red)');

  // Apaga de verdade na planilha — sem isto, a linha continuava lá e a
  // próxima busca da planilha trazia o assunto de volta como se fosse novo.
  if (APPS_SCRIPT_URL_PAUTA) {
    fetch(APPS_SCRIPT_URL_PAUTA, {
      method: 'POST',
      body: JSON.stringify({ path: 'pauta', action: 'remover', id })
    }).catch(e => console.warn('Pauta: não foi possível remover na planilha:', e.message));
  }
}

function limparAssuntos(){"""

assert content.count(old1) == 1, f"edit1: esperava 1 ocorrência, achei {content.count(old1)}"
content = content.replace(old1, new1)

# Edit 2: criarPautaGoogle -> envia o id local
old2 = """    const resp = await fetch(APPS_SCRIPT_URL_PAUTA + '?path=pauta&action=criar', {
      method: 'POST',
      body: JSON.stringify({
        assunto: item.assunto,
        descricao: item.desc,
        criador: item.criador,"""

new2 = """    const resp = await fetch(APPS_SCRIPT_URL_PAUTA + '?path=pauta&action=criar', {
      method: 'POST',
      body: JSON.stringify({
        id: item.id,
        assunto: item.assunto,
        descricao: item.desc,
        criador: item.criador,"""

assert content.count(old2) == 1, f"edit2: esperava 1 ocorrência, achei {content.count(old2)}"
content = content.replace(old2, new2)

p.write_text(content, encoding="utf-8")
print("pauta.html atualizado com sucesso.")
