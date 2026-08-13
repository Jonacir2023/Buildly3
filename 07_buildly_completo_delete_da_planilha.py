# Aplica no diretorio raiz do repo Buildly3, sobre buildly-completo.html
# Uso: python3 patch-buildly-completo-delete-da-planilha.py
import pathlib

p = pathlib.Path("buildly-completo.html")
content = p.read_text(encoding="utf-8")

# Edit 1: pautaCarregarDoServidor -> remove localmente quem já esteve
# sincronizado mas sumiu da planilha (ex.: apagado direto na planilha pelo
# usuário). Itens ainda não sincronizados (recém-criados) nunca são
# removidos por este motivo — eles legitimamente ainda não existem no
# servidor.
old1 = """async function pautaCarregarDoServidor() {
  try {
    const resp = await fetch(APPS_SCRIPT_URL + '?path=pauta&action=listar');
    const data = await resp.json();
    if (!data || (!data.dados && !data.pautas)) return;
    const doServidor = data.dados || data.pautas || [];
    const porId = new Map(pautaAssuntos.map(a => [String(a.id), a]));
    let adicionados = 0, atualizados = 0;
    doServidor.forEach(p => {
      if (!p.id) return;
      const chave = String(p.id);
      const existente = porId.get(chave);
      if (existente) {
        if (p.status && existente.status !== p.status) { existente.status = p.status; atualizados++; }
      } else {
        const novo = {
          id: p.id, assunto: p.assunto, desc: p.desc || '',
          criador: p.criador || '', resp: p.resp || '', setor: p.setor || '',
          prioridade: p.prioridade || 'media', status: p.status || 'afazer',
          dataLanc: p.dataLanc || '', dataTerm: p.dataTerm || '',
          criadoEm: Date.parse(p['Criado Em']) || Date.now(),
          // Já veio da planilha — marca como sincronizado para o ciclo
          // automático de 2 em 2 minutos não reenviar (e reduplicar) este
          // item na próxima rodada.
          _sincronizado: true
        };
        pautaAssuntos.push(novo);
        porId.set(chave, novo);
        adicionados++;
      }
    });
    if (adicionados > 0 || atualizados > 0) {
      pautaS.set('assuntos', pautaAssuntos);
      pautaRenderListar();
      console.log(`✅ Pauta: ${adicionados} novo(s), ${atualizados} atualizado(s) da planilha`);
    }
  } catch (e) {
    console.warn('Pauta: não foi possível buscar da planilha:', e.message);
  }
}"""

new1 = """async function pautaCarregarDoServidor() {
  try {
    const resp = await fetch(APPS_SCRIPT_URL + '?path=pauta&action=listar');
    const data = await resp.json();
    if (!data || (!data.dados && !data.pautas)) return;
    const doServidor = data.dados || data.pautas || [];
    const idsServidor = new Set(doServidor.map(p => String(p.id)).filter(Boolean));
    const porId = new Map(pautaAssuntos.map(a => [String(a.id), a]));
    let adicionados = 0, atualizados = 0, removidos = 0;
    doServidor.forEach(p => {
      if (!p.id) return;
      const chave = String(p.id);
      const existente = porId.get(chave);
      if (existente) {
        if (p.status && existente.status !== p.status) { existente.status = p.status; atualizados++; }
      } else {
        const novo = {
          id: p.id, assunto: p.assunto, desc: p.desc || '',
          criador: p.criador || '', resp: p.resp || '', setor: p.setor || '',
          prioridade: p.prioridade || 'media', status: p.status || 'afazer',
          dataLanc: p.dataLanc || '', dataTerm: p.dataTerm || '',
          criadoEm: Date.parse(p['Criado Em']) || Date.now(),
          // Já veio da planilha — marca como sincronizado para o ciclo
          // automático de 2 em 2 minutos não reenviar (e reduplicar) este
          // item na próxima rodada.
          _sincronizado: true
        };
        pautaAssuntos.push(novo);
        porId.set(chave, novo);
        adicionados++;
      }
    });

    // Remove localmente quem já esteve sincronizado mas sumiu da planilha —
    // ou seja, foi apagado direto na planilha. Itens ainda não
    // sincronizados (sem _sincronizado) nunca entram aqui: eles
    // legitimamente ainda não existem no servidor, então sumir da lista do
    // servidor não significa que foram apagados de propósito.
    pautaAssuntos = pautaAssuntos.filter(a => {
      if (a._sincronizado && !idsServidor.has(String(a.id))) { removidos++; return false; }
      return true;
    });

    if (adicionados > 0 || atualizados > 0 || removidos > 0) {
      pautaS.set('assuntos', pautaAssuntos);
      pautaRenderListar();
      console.log(`✅ Pauta: ${adicionados} novo(s), ${atualizados} atualizado(s), ${removidos} removido(s) da planilha`);
    }
  } catch (e) {
    console.warn('Pauta: não foi possível buscar da planilha:', e.message);
  }
}"""

assert content.count(old1) == 1, f"edit1 (pauta): esperava 1 ocorrência, achei {content.count(old1)}"
content = content.replace(old1, new1)

# Edit 2: checkinCarregarHistoricoDoServidor -> mesma correção
old2 = """    const porId = new Map(checkinAssuntos.map(a => [String(a.id), a]));
    let adicionados = 0, atualizados = 0;
    doServidor.forEach(c => {
      if (!c.id || removidosSet.has(String(c.id))) return;
      const chave = String(c.id);
      const existente = porId.get(chave);
      if (existente) {
        if (c.status && existente.status !== c.status) { existente.status = c.status; atualizados++; }
      } else {
        const novo = {
          id: c.id, assunto: c.assunto, desc: c.desc || '',
          criador: c.criador || '', resp: c.resp || '', setor: c.setor || '',
          prioridade: c.prioridade || 'media', status: c.status || 'afazer',
          dataTerm: c.dataTerm || '', concluidoEm: c.concluidoEm || '',
          criadoEm: Date.parse(c.criadoEm) || Date.now(),
          _origem: 'checkin',
          // Já veio da planilha — marca como sincronizado para o ciclo
          // automático de 2 em 2 minutos não reenviar (e reduplicar) este
          // item na próxima rodada.
          _sincronizado: true
        };
        checkinAssuntos.push(novo);
        porId.set(chave, novo);
        adicionados++;
      }
    });
    if (adicionados > 0 || atualizados > 0) {
      checkinS.set('assuntos', checkinAssuntos);
      checkinRenderCadastro();
      checkinRenderKanban();
      checkinAtualizarContadores();
      console.log(`✅ Check-in: ${adicionados} novo(s), ${atualizados} atualizado(s) da planilha`);
    }"""

new2 = """    const idsServidor = new Set(doServidor.map(c => String(c.id)).filter(Boolean));
    const porId = new Map(checkinAssuntos.map(a => [String(a.id), a]));
    let adicionados = 0, atualizados = 0, removidos = 0;
    doServidor.forEach(c => {
      if (!c.id || removidosSet.has(String(c.id))) return;
      const chave = String(c.id);
      const existente = porId.get(chave);
      if (existente) {
        if (c.status && existente.status !== c.status) { existente.status = c.status; atualizados++; }
      } else {
        const novo = {
          id: c.id, assunto: c.assunto, desc: c.desc || '',
          criador: c.criador || '', resp: c.resp || '', setor: c.setor || '',
          prioridade: c.prioridade || 'media', status: c.status || 'afazer',
          dataTerm: c.dataTerm || '', concluidoEm: c.concluidoEm || '',
          criadoEm: Date.parse(c.criadoEm) || Date.now(),
          _origem: 'checkin',
          // Já veio da planilha — marca como sincronizado para o ciclo
          // automático de 2 em 2 minutos não reenviar (e reduplicar) este
          // item na próxima rodada.
          _sincronizado: true
        };
        checkinAssuntos.push(novo);
        porId.set(chave, novo);
        adicionados++;
      }
    });

    // Remove localmente quem já esteve sincronizado mas sumiu da planilha —
    // ou seja, foi apagado direto na planilha. Itens ainda não
    // sincronizados nunca entram aqui (ver pautaCarregarDoServidor).
    checkinAssuntos = checkinAssuntos.filter(a => {
      if (a._sincronizado && !idsServidor.has(String(a.id))) { removidos++; return false; }
      return true;
    });

    if (adicionados > 0 || atualizados > 0 || removidos > 0) {
      checkinS.set('assuntos', checkinAssuntos);
      checkinRenderCadastro();
      checkinRenderKanban();
      checkinAtualizarContadores();
      console.log(`✅ Check-in: ${adicionados} novo(s), ${atualizados} atualizado(s), ${removidos} removido(s) da planilha`);
    }"""

assert content.count(old2) == 1, f"edit2 (checkin): esperava 1 ocorrência, achei {content.count(old2)}"
content = content.replace(old2, new2)

p.write_text(content, encoding="utf-8")
print("buildly-completo.html: exclusão feita direto na planilha agora remove do app também.")
