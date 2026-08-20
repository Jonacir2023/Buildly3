#!/usr/bin/env python3
"""Liga os botões Medição e Documentos na Home (antes eram "Em breve"),
adiciona a página de cada um, e cria o botão + página do novo app
Manutenção (status automático + mural da obra)."""
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


# 1) CSS do botão Manutenção
aplicar(
    '.btn-medicao{border-top-color:var(--accent)}\n'
    '.btn-docs{border-top-color:var(--accent)}',
    '.btn-medicao{border-top-color:var(--accent)}\n'
    '.btn-docs{border-top-color:var(--accent)}\n'
    '.btn-manutencao{border-top-color:var(--accent)}',
    'css-btn-manutencao',
)

# 2) Botões Medição e Documentos ativos
aplicar(
    '      <!-- 5. Medição (Reserved) -->\n'
    '      <div class="home-button btn-medicao disabled">\n'
    '        <div class="home-button-icon">📐</div>\n'
    '        <div class="home-button-title">Medição</div>\n'
    '        <div class="home-button-desc">Em desenvolvimento</div>\n'
    '        <div class="home-button-badge">Em breve</div>\n'
    '      </div>\n'
    '\n'
    '      <!-- 6. Documentos (Reserved) -->\n'
    '      <div class="home-button btn-docs disabled">\n'
    '        <div class="home-button-icon">📄</div>\n'
    '        <div class="home-button-title">Documentos</div>\n'
    '        <div class="home-button-desc">Em desenvolvimento</div>\n'
    '        <div class="home-button-badge">Em breve</div>\n'
    '      </div>',
    '      <!-- 5. Medição -->\n'
    '      <div class="home-button btn-medicao" onclick="switchTab(\'medicao\', this)">\n'
    '        <div class="home-button-icon">📐</div>\n'
    '        <div class="home-button-title">Medição</div>\n'
    '        <div class="home-button-desc">Cliente e terceiros</div>\n'
    '      </div>\n'
    '\n'
    '      <!-- 6. Documentos -->\n'
    '      <div class="home-button btn-docs" onclick="switchTab(\'documentos\', this)">\n'
    '        <div class="home-button-icon">📄</div>\n'
    '        <div class="home-button-title">Documentos</div>\n'
    '        <div class="home-button-desc">Contrato e orçamento</div>\n'
    '      </div>',
    'botoes-medicao-documentos',
)

# 3) Botão Manutenção (10º botão) — logo após Resumo do Tempo
aplicar(
    '      <div class="home-button-title">Resumo do Tempo</div>\n'
    '        <div class="home-button-desc">Condições climáticas</div>\n'
    '      </div>\n'
    '    </div>',
    '      <div class="home-button-title">Resumo do Tempo</div>\n'
    '        <div class="home-button-desc">Condições climáticas</div>\n'
    '      </div>\n'
    '\n'
    '      <!-- 10. Manutenção -->\n'
    '      <div class="home-button btn-manutencao" onclick="switchTab(\'manutencao\', this)">\n'
    '        <div class="home-button-icon">🛠️</div>\n'
    '        <div class="home-button-title">Manutenção</div>\n'
    '        <div class="home-button-desc">Status e mural da obra</div>\n'
    '      </div>\n'
    '    </div>',
    'botao-manutencao',
)

# 4) Páginas com os iframes dos 3 apps
aplicar(
    '<!-- OBRA PAGE (cadastro compartilhado entre todos os apps) -->',
    '<!-- MEDIÇÃO PAGE (medições com cliente e terceiros) -->\n'
    '<div class="page" id="page-medicao">\n'
    '  <iframe id="medicao-iframe" src="medicoes.html" style="width:100%;height:calc(100vh - 140px);border:none;background:#f0ece7;display:block;margin:0;padding:0" frameborder="0" allow="geolocation; microphone; camera"></iframe>\n'
    '</div>\n'
    '\n'
    '<!-- DOCUMENTOS PAGE (contrato, cronograma, orçamento + alertas) -->\n'
    '<div class="page" id="page-documentos">\n'
    '  <iframe id="documentos-iframe" src="documentos.html" style="width:100%;height:calc(100vh - 140px);border:none;background:#f0ece7;display:block;margin:0;padding:0" frameborder="0" allow="geolocation; microphone; camera"></iframe>\n'
    '</div>\n'
    '\n'
    '<!-- MANUTENÇÃO PAGE (painel de status + mural da obra) -->\n'
    '<div class="page" id="page-manutencao">\n'
    '  <iframe id="manutencao-iframe" src="manutencao.html" style="width:100%;height:calc(100vh - 140px);border:none;background:#f0ece7;display:block;margin:0;padding:0" frameborder="0" allow="geolocation; microphone; camera"></iframe>\n'
    '</div>\n'
    '\n'
    '<!-- OBRA PAGE (cadastro compartilhado entre todos os apps) -->',
    'iframes-3-apps',
)

# 5) switchTab(): atualizar o iframe da Manutenção sozinho ao abrir a aba
aplicar(
    "  } else if (tab === 'resumo-tempo') {\n"
    "    const ifr = document.getElementById('resumo-tempo-iframe');\n"
    "    if (ifr && ifr.contentWindow && ifr.contentWindow.atualizarResumoTempo) {\n"
    "      ifr.contentWindow.atualizarResumoTempo();\n"
    "    }\n"
    "  }\n"
    "}",
    "  } else if (tab === 'resumo-tempo') {\n"
    "    const ifr = document.getElementById('resumo-tempo-iframe');\n"
    "    if (ifr && ifr.contentWindow && ifr.contentWindow.atualizarResumoTempo) {\n"
    "      ifr.contentWindow.atualizarResumoTempo();\n"
    "    }\n"
    "  } else if (tab === 'manutencao') {\n"
    "    const ifr = document.getElementById('manutencao-iframe');\n"
    "    if (ifr && ifr.contentWindow && ifr.contentWindow.atualizarManutencao) {\n"
    "      ifr.contentWindow.atualizarManutencao();\n"
    "    }\n"
    "  }\n"
    "}",
    'switchtab-manutencao',
)

alvo.write_text(content, encoding='utf-8')
print(f'OK: {aplicadas} mudança(s) aplicada(s), {ja_aplicadas} já estavam aplicadas em {alvo}')
