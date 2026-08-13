# Aplica no diretorio raiz do repo Buildly3, sobre buildly-completo.html
# Uso: python3 patch-buildly-completo-antiduplicacao.py
import pathlib

p = pathlib.Path("buildly-completo.html")
content = p.read_text(encoding="utf-8")

# Edit 1: pautaCarregarDoServidor -> marca itens vindos do servidor como já
# sincronizados. Sem isto, o ciclo automático de 2 em 2 minutos
# (sincronizarComGoogleSheets) via _sincronizado ausente reenviava esses
# itens como "criar" de novo, e cada reenvio criava outra linha na planilha
# (mesmo com o ID indo junto) porque criarPauta só sabia "appendRow".
old1 = """        const novo = {
          id: p.id, assunto: p.assunto, desc: p.desc || '',
          criador: p.criador || '', resp: p.resp || '', setor: p.setor || '',
          prioridade: p.prioridade || 'media', status: p.status || 'afazer',
          dataLanc: p.dataLanc || '', dataTerm: p.dataTerm || '',
          criadoEm: Date.parse(p['Criado Em']) || Date.now()
        };
        pautaAssuntos.push(novo);"""

new1 = """        const novo = {
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
        pautaAssuntos.push(novo);"""

assert content.count(old1) == 1, f"edit1: esperava 1 ocorrência, achei {content.count(old1)}"
content = content.replace(old1, new1)

# Edit 2: checkinCarregarHistoricoDoServidor -> mesma correção
old2 = """        const novo = {
          id: c.id, assunto: c.assunto, desc: c.desc || '',
          criador: c.criador || '', resp: c.resp || '', setor: c.setor || '',
          prioridade: c.prioridade || 'media', status: c.status || 'afazer',
          dataTerm: c.dataTerm || '', concluidoEm: c.concluidoEm || '',
          criadoEm: Date.parse(c.criadoEm) || Date.now(),
          _origem: 'checkin'
        };
        checkinAssuntos.push(novo);"""

new2 = """        const novo = {
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
        checkinAssuntos.push(novo);"""

assert content.count(old2) == 1, f"edit2: esperava 1 ocorrência, achei {content.count(old2)}"
content = content.replace(old2, new2)

p.write_text(content, encoding="utf-8")
print("buildly-completo.html: correção anti-duplicação aplicada com sucesso.")
