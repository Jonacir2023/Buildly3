#!/usr/bin/env python3
"""Adiciona marcação por dia (ponto) no Calendário do Check-in: cada dia com
assunto lançado ganha um ponto; clicar no dia mostra os assuntos daquele dia
no resumo abaixo do calendário, no mesmo formato da aba Cadastro."""
import pathlib
import sys

pasta = pathlib.Path(__file__).resolve().parent
alvo = pasta / 'buildly-completo.html'
if not alvo.exists():
    alvo = pasta.parent / 'buildly-completo.html'
if not alvo.exists():
    alvo = pathlib.Path.cwd() / 'buildly-completo.html'
if not alvo.exists():
    print('ERRO: buildly-completo.html não encontrado'); sys.exit(1)

content = alvo.read_text(encoding='utf-8')
aplicadas = 0
ja_aplicadas = 0

replacements = [
    (
        ".cal-day{aspect-ratio:1;display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius:6px;font-size:13px;font-weight:600;cursor:pointer;transition:background .15s;background:#fff;border:1px solid var(--line)}\n"
        ".cal-day.today{background:var(--accent);color:#fff;border-color:var(--accent)}\n"
        ".cal-day.has-event{border-color:var(--blue);background:#dde8f5}\n"
        ".cal-day.empty{background:transparent;border-color:transparent;cursor:default}",
        ".cal-day{position:relative;aspect-ratio:1;display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius:6px;font-size:13px;font-weight:600;cursor:pointer;transition:background .15s;background:#fff;border:1px solid var(--line)}\n"
        ".cal-day.today{background:var(--accent);color:#fff;border-color:var(--accent)}\n"
        ".cal-day.has-event{border-color:var(--blue);background:#dde8f5}\n"
        ".cal-day.selected{outline:2px solid var(--blue);outline-offset:-1px}\n"
        ".cal-day.empty{background:transparent;border-color:transparent;cursor:default}\n"
        ".cal-day-dot{width:5px;height:5px;border-radius:50%;background:var(--blue);position:absolute;bottom:4px;left:50%;transform:translateX(-50%)}\n"
        ".cal-day.today .cal-day-dot{background:#fff}",
        'marcador-checkin-01',
    ),
    (
        '      <div class="cal-grid" id="checkin-cal-grid"></div>\n'
        '    </div>\n'
        '    <div class="sec">\n'
        '      <div class="sec-title">📅 Reuniões do Mês</div>\n'
        '      <div id="checkin-lista-reunioes-cal"></div>\n'
        '    </div>\n'
        '  </div>',
        '      <div class="cal-grid" id="checkin-cal-grid"></div>\n'
        '    </div>\n'
        '    <div class="sec" id="checkin-cal-resumo-dia-sec" style="display:none">\n'
        '      <div class="sec-title" id="checkin-cal-resumo-dia-titulo">📌 Assuntos do dia</div>\n'
        '      <div id="checkin-cal-resumo-dia-lista"></div>\n'
        '    </div>\n'
        '    <div class="sec">\n'
        '      <div class="sec-title">📅 Reuniões do Mês</div>\n'
        '      <div id="checkin-lista-reunioes-cal"></div>\n'
        '    </div>\n'
        '  </div>',
        'marcador-checkin-02',
    ),
    (
        "function checkinRenderCadastro() {\n"
        "  const cont = document.getElementById('checkin-lista-assuntos-cadastro');\n"
        "  if (!checkinAssuntos.length) {\n"
        "    cont.innerHTML = '<div class=\"empty-state\"><div class=\"empty-state-icon\">📋</div><div class=\"empty-state-txt\">Nenhum</div></div>';\n"
        "    return;\n"
        "  }\n"
        "  cont.innerHTML = checkinAssuntos.map(a => `\n"
        "    <div style=\"background:#fff;border-radius:8px;padding:11px 12px;margin-bottom:8px;border:1px solid var(--line)\">\n"
        "      <div style=\"display:flex;align-items:flex-start;gap:8px\">\n"
        "        <div style=\"flex:1\">\n"
        "          <div style=\"font-family:var(--serif);font-weight:700;font-size:15px;margin-bottom:4px\">${a.assunto}</div>\n"
        "          <div style=\"display:flex;gap:4px;flex-wrap:wrap;margin-bottom:4px\">\n"
        "            <span class=\"badge ${checkinPriorCor(a.prioridade)}\">${a.prioridade}</span>\n"
        "            ${a.setor ? `<span class=\"badge badge-blue\">${a.setor}</span>` : ''}\n"
        "            <span class=\"badge ${checkinStatusBadge(a.status)}\">${checkinStatusLabel(a.status)}</span>\n"
        "          </div>\n"
        "          <div style=\"font-size:11px;color:var(--ink-faint)\">\n"
        "            ${a.dataLanc ? `📅 Lançamento: ${checkinFormatDate(a.dataLanc)}` : ''}\n"
        "            ${a.dataTerm ? ` &nbsp;|&nbsp; 🏁 Término: ${checkinFormatDate(a.dataTerm)}` : ''}\n"
        "          </div>\n"
        "          ${a.resp ? `<div style=\"font-size:11px;color:var(--ink-soft);margin-top:2px\">👤 Resp: ${a.resp}</div>` : ''}\n"
        "          ${a.criador ? `<div style=\"font-size:11px;color:var(--ink-faint);margin-top:1px\">✍️ Criador: ${a.criador}</div>` : ''}\n"
        "        </div>\n"
        "        <div style=\"display:flex;gap:4px;flex-shrink:0\">\n"
        "          <button class=\"card-btn\" onclick=\"checkinEditarAssunto('${a.id}')\">✏️</button>\n"
        "          <button class=\"card-btn\" onclick=\"checkinRemoverAssunto('${a.id}')\">🗑️</button>\n"
        "        </div>\n"
        "      </div>\n"
        "    </div>\n"
        "  `).join('');\n"
        "}",
        "function checkinCardAssuntoHTML(a) {\n"
        "  return `\n"
        "    <div style=\"background:#fff;border-radius:8px;padding:11px 12px;margin-bottom:8px;border:1px solid var(--line)\">\n"
        "      <div style=\"display:flex;align-items:flex-start;gap:8px\">\n"
        "        <div style=\"flex:1\">\n"
        "          <div style=\"font-family:var(--serif);font-weight:700;font-size:15px;margin-bottom:4px\">${a.assunto}</div>\n"
        "          <div style=\"display:flex;gap:4px;flex-wrap:wrap;margin-bottom:4px\">\n"
        "            <span class=\"badge ${checkinPriorCor(a.prioridade)}\">${a.prioridade}</span>\n"
        "            ${a.setor ? `<span class=\"badge badge-blue\">${a.setor}</span>` : ''}\n"
        "            <span class=\"badge ${checkinStatusBadge(a.status)}\">${checkinStatusLabel(a.status)}</span>\n"
        "          </div>\n"
        "          <div style=\"font-size:11px;color:var(--ink-faint)\">\n"
        "            ${a.dataLanc ? `📅 Lançamento: ${checkinFormatDate(a.dataLanc)}` : ''}\n"
        "            ${a.dataTerm ? ` &nbsp;|&nbsp; 🏁 Término: ${checkinFormatDate(a.dataTerm)}` : ''}\n"
        "          </div>\n"
        "          ${a.resp ? `<div style=\"font-size:11px;color:var(--ink-soft);margin-top:2px\">👤 Resp: ${a.resp}</div>` : ''}\n"
        "          ${a.criador ? `<div style=\"font-size:11px;color:var(--ink-faint);margin-top:1px\">✍️ Criador: ${a.criador}</div>` : ''}\n"
        "        </div>\n"
        "        <div style=\"display:flex;gap:4px;flex-shrink:0\">\n"
        "          <button class=\"card-btn\" onclick=\"checkinEditarAssunto('${a.id}')\">✏️</button>\n"
        "          <button class=\"card-btn\" onclick=\"checkinRemoverAssunto('${a.id}')\">🗑️</button>\n"
        "        </div>\n"
        "      </div>\n"
        "    </div>\n"
        "  `;\n"
        "}\n"
        "\n"
        "function checkinRenderCadastro() {\n"
        "  const cont = document.getElementById('checkin-lista-assuntos-cadastro');\n"
        "  if (!checkinAssuntos.length) {\n"
        "    cont.innerHTML = '<div class=\"empty-state\"><div class=\"empty-state-icon\">📋</div><div class=\"empty-state-txt\">Nenhum</div></div>';\n"
        "    return;\n"
        "  }\n"
        "  cont.innerHTML = checkinAssuntos.map(checkinCardAssuntoHTML).join('');\n"
        "}",
        'marcador-checkin-03',
    ),
    (
        "let checkinCalMes = new Date();",
        "let checkinCalMes = new Date();\n"
        "let checkinDiaSelecionadoCal = null;",
        'marcador-checkin-04',
    ),
    (
        "function checkinRenderCalendario() {\n"
        "  const ano = checkinCalMes.getFullYear(), mes = checkinCalMes.getMonth();\n"
        "  document.getElementById('checkin-cal-titulo').textContent = checkinCalMes.toLocaleDateString('pt-BR', {month:'long',year:'numeric'}).replace(/^\\w/, c => c.toUpperCase());\n"
        "  const primeiroDia = new Date(ano, mes, 1).getDay();\n"
        "  const diasMes = new Date(ano, mes + 1, 0).getDate();\n"
        "  const hoje = new Date();\n"
        "  const eventosDias = {};\n"
        "  checkinReunioes.forEach(r => {\n"
        "    if (!r.data) return;\n"
        "    const [a,m,d] = r.data.split('-').map(Number);\n"
        "    if (m - 1 === mes && a === ano) eventosDias[d] = (eventosDias[d] || 0) + 1;\n"
        "  });\n"
        "  const dias = ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb'];\n"
        "  let html = dias.map(d => `<div class=\"cal-day-name\">${d}</div>`).join('');\n"
        "  for (let i = 0; i < primeiroDia; i++) html += `<div class=\"cal-day empty\"></div>`;\n"
        "  for (let d = 1; d <= diasMes; d++) {\n"
        "    const isHoje = d === hoje.getDate() && mes === hoje.getMonth() && ano === hoje.getFullYear();\n"
        "    html += `<div class=\"cal-day ${isHoje ? 'today' : ''} ${eventosDias[d] ? 'has-event' : ''}\">${d}</div>`;\n"
        "  }\n"
        "  document.getElementById('checkin-cal-grid').innerHTML = html;",

        "function checkinRenderCalendario() {\n"
        "  const ano = checkinCalMes.getFullYear(), mes = checkinCalMes.getMonth();\n"
        "  document.getElementById('checkin-cal-titulo').textContent = checkinCalMes.toLocaleDateString('pt-BR', {month:'long',year:'numeric'}).replace(/^\\w/, c => c.toUpperCase());\n"
        "  const primeiroDia = new Date(ano, mes, 1).getDay();\n"
        "  const diasMes = new Date(ano, mes + 1, 0).getDate();\n"
        "  const hoje = new Date();\n"
        "  const assuntosDias = {};\n"
        "  checkinAssuntos.forEach(a => {\n"
        "    if (!a.dataLanc) return;\n"
        "    const [ay,am,ad] = a.dataLanc.split('-').map(Number);\n"
        "    if (am - 1 === mes && ay === ano) assuntosDias[ad] = (assuntosDias[ad] || 0) + 1;\n"
        "  });\n"
        "  const dias = ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb'];\n"
        "  let html = dias.map(d => `<div class=\"cal-day-name\">${d}</div>`).join('');\n"
        "  for (let i = 0; i < primeiroDia; i++) html += `<div class=\"cal-day empty\"></div>`;\n"
        "  for (let d = 1; d <= diasMes; d++) {\n"
        "    const iso = `${ano}-${String(mes + 1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;\n"
        "    const isHoje = d === hoje.getDate() && mes === hoje.getMonth() && ano === hoje.getFullYear();\n"
        "    const isSelecionado = iso === checkinDiaSelecionadoCal;\n"
        "    html += `<div class=\"cal-day ${isHoje ? 'today' : ''} ${isSelecionado ? 'selected' : ''}\" onclick=\"checkinSelecionarDiaCal('${iso}')\">${d}${assuntosDias[d] ? '<div class=\"cal-day-dot\"></div>' : ''}</div>`;\n"
        "  }\n"
        "  document.getElementById('checkin-cal-grid').innerHTML = html;",
        'marcador-checkin-05',
    ),
    (
        "  `).join('') : '<div class=\"empty-state\"><div class=\"empty-state-icon\">📭</div><div class=\"empty-state-txt\">Nenhuma reunião</div></div>';\n"
        "}\n"
        "\n"
        "function checkinCalNav(dir) {\n"
        "  checkinCalMes = new Date(checkinCalMes.getFullYear(), checkinCalMes.getMonth() + dir, 1);\n"
        "  checkinRenderCalendario();\n"
        "}",
        "  `).join('') : '<div class=\"empty-state\"><div class=\"empty-state-icon\">📭</div><div class=\"empty-state-txt\">Nenhuma reunião</div></div>';\n"
        "}\n"
        "\n"
        "function checkinSelecionarDiaCal(iso) {\n"
        "  checkinDiaSelecionadoCal = iso;\n"
        "  checkinRenderCalendario();\n"
        "  const [ay, am, ad] = iso.split('-');\n"
        "  const lista = checkinAssuntos.filter(a => a.dataLanc === iso);\n"
        "  document.getElementById('checkin-cal-resumo-dia-titulo').textContent = `📌 Assuntos de ${ad}/${am}/${ay}`;\n"
        "  document.getElementById('checkin-cal-resumo-dia-lista').innerHTML = lista.length\n"
        "    ? lista.map(checkinCardAssuntoHTML).join('')\n"
        "    : '<div class=\"empty-state\"><div class=\"empty-state-icon\">📋</div><div class=\"empty-state-txt\">Nenhum assunto criado nesse dia</div></div>';\n"
        "  const sec = document.getElementById('checkin-cal-resumo-dia-sec');\n"
        "  sec.style.display = '';\n"
        "  sec.scrollIntoView({behavior:'smooth', block:'nearest'});\n"
        "}\n"
        "\n"
        "function checkinCalNav(dir) {\n"
        "  checkinCalMes = new Date(checkinCalMes.getFullYear(), checkinCalMes.getMonth() + dir, 1);\n"
        "  checkinDiaSelecionadoCal = null;\n"
        "  document.getElementById('checkin-cal-resumo-dia-sec').style.display = 'none';\n"
        "  checkinRenderCalendario();\n"
        "}",
        'marcador-checkin-06',
    ),
]

for old, new, nome in replacements:
    if new in content:
        ja_aplicadas += 1
    elif old in content:
        content = content.replace(old, new, 1)
        aplicadas += 1
    else:
        print(f'AVISO: trecho "{nome}" não encontrado (arquivo pode já estar diferente). Pulando.')

alvo.write_text(content, encoding='utf-8')
print(f'OK: {aplicadas} mudança(s) aplicada(s), {ja_aplicadas} já estavam aplicadas em {alvo}')
