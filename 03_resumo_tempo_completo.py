#!/usr/bin/env python3
"""Publica de vez o app Resumo do Tempo (mapa mensal + PDF + WhatsApp) e a
ferramenta de remover dados de obra errada — nenhum dos dois tinha sido
aplicado ainda em buildly-completo.html."""
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


def aplicar(old, new, nome):
    global content, aplicadas, ja_aplicadas
    if new in content:
        ja_aplicadas += 1
        return
    if old not in content:
        print(f'AVISO: trecho "{nome}" não encontrado. Pulando.')
        return
    content = content.replace(old, new, 1)
    aplicadas += 1


# 1) Botão "Resumo do Tempo" na Home
aplicar(
    '      <!-- 9. Resumo do Tempo (Reserved) -->\n'
    '      <div class="home-button btn-tempo disabled">\n'
    '        <div class="home-button-icon">🌦️</div>\n'
    '        <div class="home-button-title">Resumo do Tempo</div>\n'
    '        <div class="home-button-desc">Em desenvolvimento</div>\n'
    '        <div class="home-button-badge">Em breve</div>\n'
    '      </div>',
    '      <!-- 9. Resumo do Tempo -->\n'
    '      <div class="home-button btn-tempo" onclick="switchTab(\'resumo-tempo\', this)">\n'
    '        <div class="home-button-icon">🌦️</div>\n'
    '        <div class="home-button-title">Resumo do Tempo</div>\n'
    '        <div class="home-button-desc">Condições climáticas</div>\n'
    '      </div>',
    'botao-resumo-tempo',
)

# 2) Página do iframe do Resumo do Tempo
aplicar(
    '<!-- OBRA PAGE (cadastro compartilhado entre todos os apps) -->',
    '<!-- RESUMO DO TEMPO PAGE (condições climáticas, alimentado pelo RDO) -->\n'
    '<div class="page" id="page-resumo-tempo">\n'
    '  <iframe id="resumo-tempo-iframe" src="resumo-tempo.html" style="width:100%;height:calc(100vh - 140px);border:none;background:#f0ece7;display:block;margin:0;padding:0" frameborder="0" allow="geolocation; microphone; camera"></iframe>\n'
    '</div>\n'
    '\n'
    '<!-- OBRA PAGE (cadastro compartilhado entre todos os apps) -->',
    'iframe-resumo-tempo',
)

# 3) Seção "Remover dados de outra obra" na tela Obras
aplicar(
    '      <div class="frow"><label>Encerramento sábado</label><input type="time" id="obra-encerramento-sabado" value="16:00"/></div>\n'
    '      <button class="btn btn-primary btn-full" onclick="obraSalvar()">💾 SALVAR OBRA</button>\n'
    '    </div>\n'
    '  </div>\n'
    '</div>',
    '      <div class="frow"><label>Encerramento sábado</label><input type="time" id="obra-encerramento-sabado" value="16:00"/></div>\n'
    '      <button class="btn btn-primary btn-full" onclick="obraSalvar()">💾 SALVAR OBRA</button>\n'
    '    </div>\n'
    '\n'
    '    <div class="sec" style="border-color:var(--red)">\n'
    '      <div class="sec-title" style="color:var(--red)">🧹 Remover dados de outra obra</div>\n'
    '      <p style="font-size:12px;color:var(--ink-faint);margin-bottom:8px">\n'
    '        Use apenas se o Diário de Obras (RDO) de uma obra ERRADA (ex.: um backup\n'
    '        importado por engano) ficou salvo neste navegador. Isso apaga só o RDO\n'
    '        daquela obra específica — não mexe na obra atual nem em Pauta/Check-in.\n'
    '      </p>\n'
    '      <div id="obra-remover-lista" style="font-size:11px;color:var(--ink-faint);margin-bottom:8px"></div>\n'
    '      <input type="text" id="obra-remover-nome" placeholder="Nome exato da obra a remover (ex.: Suzano)"/>\n'
    '      <button class="btn btn-outline btn-sm" style="color:var(--red);border-color:var(--red);margin-top:8px" onclick="obraRemoverDadosDeOutraObra()">🗑️ Apagar RDO dessa obra</button>\n'
    '    </div>\n'
    '  </div>\n'
    '</div>',
    'secao-remover-obra',
)

# 4) switchTab(): atualizar o iframe do Resumo do Tempo sozinho ao abrir a aba
aplicar(
    "  } else if (tab === 'obra') {\n"
    "    obraInit();\n"
    "  }\n"
    "}",
    "  } else if (tab === 'obra') {\n"
    "    obraInit();\n"
    "  } else if (tab === 'resumo-tempo') {\n"
    "    const ifr = document.getElementById('resumo-tempo-iframe');\n"
    "    if (ifr && ifr.contentWindow && ifr.contentWindow.atualizarResumoTempo) {\n"
    "      ifr.contentWindow.atualizarResumoTempo();\n"
    "    }\n"
    "  }\n"
    "}",
    'switchtab-resumo-tempo',
)

# 5) JS: obraListarSalvas() + obraRemoverDadosDeOutraObra()
aplicar(
    "  document.getElementById('obra-encerramento-sabado').value = o.encerramentoSabado || '16:00';\n"
    "  obraRenderLogoPreview(o.logo);\n"
    "}",
    "  document.getElementById('obra-encerramento-sabado').value = o.encerramentoSabado || '16:00';\n"
    "  obraRenderLogoPreview(o.logo);\n"
    "  obraListarSalvas();\n"
    "}\n"
    "\n"
    "// Lista os nomes de obra que têm um Diário de Obras (RDO) salvo neste\n"
    "// navegador, para ajudar a identificar o nome exato antes de remover.\n"
    "function obraListarSalvas() {\n"
    "  const el = document.getElementById('obra-remover-lista');\n"
    "  if (!el) return;\n"
    "  const nomes = [];\n"
    "  for (let i = 0; i < localStorage.length; i++) {\n"
    "    const k = localStorage.key(i);\n"
    "    if (k && k.indexOf('diario_obras_v4_state_') === 0) {\n"
    "      let nome = k.replace('diario_obras_v4_state_', '');\n"
    "      try {\n"
    "        const s = JSON.parse(localStorage.getItem(k));\n"
    "        if (s && s.obra && s.obra.nome) nome = s.obra.nome;\n"
    "      } catch (e) { /* mantém o slug como nome */ }\n"
    "      nomes.push(nome);\n"
    "    }\n"
    "  }\n"
    "  el.textContent = nomes.length\n"
    "    ? 'RDOs salvos neste navegador: ' + nomes.join(', ')\n"
    "    : 'Nenhum RDO salvo neste navegador ainda.';\n"
    "}\n"
    "\n"
    "// Apaga o Diário de Obras (estado + histórico) de UMA obra específica,\n"
    "// identificada pelo nome. Não mexe na obra atualmente em uso nem em\n"
    "// Pauta/Check-in — só remove as chaves 'diario_obras_v4_*' daquele nome.\n"
    "function obraRemoverDadosDeOutraObra() {\n"
    "  const campo = document.getElementById('obra-remover-nome');\n"
    "  const nome = (campo.value || '').trim();\n"
    "  if (!nome) { obraNotify('Digite o nome exato da obra a remover', 'var(--red)'); return; }\n"
    "  const slug = nome.replace(/\\s+/g, '_').toLowerCase();\n"
    "  const chaves = ['diario_obras_v4_state_' + slug, 'diario_obras_v4_history_' + slug];\n"
    "  const existentes = chaves.filter(k => localStorage.getItem(k) !== null);\n"
    "  if (!existentes.length) { obraNotify('Nenhum RDO encontrado com o nome \"' + nome + '\"', 'var(--red)'); return; }\n"
    "  if (!confirm(`Isso vai apagar PERMANENTEMENTE o Diário de Obras (RDO) salvo com o nome \"${nome}\" neste navegador. Não tem como desfazer. Confirma?`)) return;\n"
    "  existentes.forEach(k => localStorage.removeItem(k));\n"
    "  campo.value = '';\n"
    "  obraListarSalvas();\n"
    "  obraNotify('✓ Dados de \"' + nome + '\" apagados');\n"
    "}",
    'js-remover-obra',
)

alvo.write_text(content, encoding='utf-8')
print(f'OK: {aplicadas} mudança(s) aplicada(s), {ja_aplicadas} já estavam aplicadas em {alvo}')
