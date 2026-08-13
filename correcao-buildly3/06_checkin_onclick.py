# Aplica no diretorio raiz do repo Buildly3, sobre Check-in.html
# Uso: python3 patch-checkin-onclick-ids.py
import pathlib

p = pathlib.Path("Check-in.html")
content = p.read_text(encoding="utf-8")

# Mesmo bug do buildly-completo.html: onclick="fn(${a.id})" sem aspas.
# Funcionava por acidente enquanto os IDs eram numeros puros (Date.now()).
# Agora que IDs vindos da planilha sao textos tipo "CHECKIN-1755043265123",
# o atributo vira JS invalido e quebra com "ReferenceError: CHECKIN is not
# defined" assim que o botao e clicado — nenhum botao (mover, editar, excluir)
# fazia qualquer coisa.

old1 = """                ${c.status==='afazer'?`<button class="card-btn" onclick="moverCard(${a.id},'fazendo')" title="Iniciar">⚡</button>`:''}
                ${c.status!=='concluido'?`<button class="card-btn" onclick="moverCard(${a.id},'concluido')" title="Concluir">✅</button>`:''}
                ${c.status!=='cancelado'&&c.status!=='concluido'?`<button class="card-btn" onclick="moverCard(${a.id},'cancelado')" title="Cancelar">🚫</button>`:''}
                <button class="card-btn" onclick="editarAssunto(${a.id})" title="Editar">✏️</button>"""

new1 = """                ${c.status==='afazer'?`<button class="card-btn" onclick="moverCard('${a.id}','fazendo')" title="Iniciar">⚡</button>`:''}
                ${c.status!=='concluido'?`<button class="card-btn" onclick="moverCard('${a.id}','concluido')" title="Concluir">✅</button>`:''}
                ${c.status!=='cancelado'&&c.status!=='concluido'?`<button class="card-btn" onclick="moverCard('${a.id}','cancelado')" title="Cancelar">🚫</button>`:''}
                <button class="card-btn" onclick="editarAssunto('${a.id}')" title="Editar">✏️</button>"""

assert content.count(old1) == 1, f"edit1 (kanban): esperava 1 ocorrência, achei {content.count(old1)}"
content = content.replace(old1, new1)

old2 = """          <button class="card-btn" onclick="editarAssunto(${a.id})" title="Editar">✏️</button>
          <button class="card-btn" onclick="removerAssunto(${a.id})" title="Remover">🗑️</button>"""

new2 = """          <button class="card-btn" onclick="editarAssunto('${a.id}')" title="Editar">✏️</button>
          <button class="card-btn" onclick="removerAssunto('${a.id}')" title="Remover">🗑️</button>"""

assert content.count(old2) == 1, f"edit2 (cadastro): esperava 1 ocorrência, achei {content.count(old2)}"
content = content.replace(old2, new2)

# Comparações de ID precisam ser seguras a tipo agora que o onclick sempre
# manda uma string, mas o ID guardado pode ser um número (itens antigos,
# criados localmente com Date.now()).
old3 = "function moverCard(id,status){\n  const a=assuntos.find(x=>x.id===id);"
new3 = "function moverCard(id,status){\n  const a=assuntos.find(x=>String(x.id)===String(id));"
assert content.count(old3) == 1, f"edit3 (moverCard): esperava 1 ocorrência, achei {content.count(old3)}"
content = content.replace(old3, new3)

old4 = "function editarAssunto(id){abrirModalAssunto(assuntos.find(x=>x.id===id))}"
new4 = "function editarAssunto(id){abrirModalAssunto(assuntos.find(x=>String(x.id)===String(id)))}"
assert content.count(old4) == 1, f"edit4 (editarAssunto): esperava 1 ocorrência, achei {content.count(old4)}"
content = content.replace(old4, new4)

old5 = "  assuntos=assuntos.filter(a=>a.id!==id);"
new5 = "  assuntos=assuntos.filter(a=>String(a.id)!==String(id));"
assert content.count(old5) == 1, f"edit5 (removerAssunto): esperava 1 ocorrência, achei {content.count(old5)}"
content = content.replace(old5, new5)

p.write_text(content, encoding="utf-8")
print("Check-in.html: correção dos botões (onclick sem aspas + comparação de ID) aplicada com sucesso.")
