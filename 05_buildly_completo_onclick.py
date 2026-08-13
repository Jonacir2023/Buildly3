# Aplica no diretorio raiz do repo Buildly3, sobre buildly-completo.html
# Uso: python3 patch-buildly-completo-onclick-ids.py
import pathlib

p = pathlib.Path("buildly-completo.html")
content = p.read_text(encoding="utf-8")

# Os botoes do Kanban e do Cadastro do Check-in montavam onclick="fn(${a.id})"
# SEM aspas. Enquanto os IDs eram numeros puros (Date.now()) isso funcionava
# por acidente. Agora que os IDs vindos da planilha sao textos como
# "CHECKIN-1755043265123" ou "PAUTA-1755043265123", o atributo onclick vira
# JS invalido: checkinRemoverAssunto(CHECKIN-1755043265123) e o navegador
# tenta interpretar "CHECKIN" como uma variavel e quebra com
# "ReferenceError: CHECKIN is not defined" antes mesmo de chamar a funcao —
# por isso nenhum botao (editar, mover, excluir) fazia qualquer coisa.

old = """                ${c.status === 'afazer' ? `<button class="card-btn" onclick="checkinMoverCard(${a.id},'fazendo')" title="Iniciar">⚡</button>` : ''}
                ${c.status !== 'concluido' ? `<button class="card-btn" onclick="checkinMoverCard(${a.id},'concluido')" title="Concluir">✅</button>` : ''}
                ${c.status !== 'cancelado' && c.status !== 'concluido' ? `<button class="card-btn" onclick="checkinMoverCard(${a.id},'cancelado')" title="Cancelar">🚫</button>` : ''}
                <button class="card-btn" onclick="checkinEditarAssunto(${a.id})" title="Editar">✏️</button>"""

new = """                ${c.status === 'afazer' ? `<button class="card-btn" onclick="checkinMoverCard('${a.id}','fazendo')" title="Iniciar">⚡</button>` : ''}
                ${c.status !== 'concluido' ? `<button class="card-btn" onclick="checkinMoverCard('${a.id}','concluido')" title="Concluir">✅</button>` : ''}
                ${c.status !== 'cancelado' && c.status !== 'concluido' ? `<button class="card-btn" onclick="checkinMoverCard('${a.id}','cancelado')" title="Cancelar">🚫</button>` : ''}
                <button class="card-btn" onclick="checkinEditarAssunto('${a.id}')" title="Editar">✏️</button>"""

assert content.count(old) == 1, f"edit1 (kanban): esperava 1 ocorrência, achei {content.count(old)}"
content = content.replace(old, new)

old2 = """          <button class="card-btn" onclick="checkinEditarAssunto(${a.id})">✏️</button>
          <button class="card-btn" onclick="checkinRemoverAssunto(${a.id})">🗑️</button>"""

new2 = """          <button class="card-btn" onclick="checkinEditarAssunto('${a.id}')">✏️</button>
          <button class="card-btn" onclick="checkinRemoverAssunto('${a.id}')">🗑️</button>"""

assert content.count(old2) == 1, f"edit2 (cadastro): esperava 1 ocorrência, achei {content.count(old2)}"
content = content.replace(old2, new2)

p.write_text(content, encoding="utf-8")
print("buildly-completo.html: correção dos botões (onclick sem aspas) aplicada com sucesso.")
