#!/usr/bin/env python3
"""Home: adiciona os botões Reuniões e Resumo do Tempo ao lado de Obras
(placeholders 'Em breve', mesmo padrão de Medição/Documentos)."""
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

old = (
    '      <!-- 7. Obras -->\n'
    '      <div class="home-button btn-obras" onclick="switchTab(\'obra\', this)">\n'
    '        <div class="home-button-icon">🏢</div>\n'
    '        <div class="home-button-title">Obras</div>\n'
    '        <div class="home-button-desc">Cadastrar e editar obras</div>\n'
    '      </div>\n'
    '    </div>'
)
new = (
    '      <!-- 7. Obras -->\n'
    '      <div class="home-button btn-obras" onclick="switchTab(\'obra\', this)">\n'
    '        <div class="home-button-icon">🏢</div>\n'
    '        <div class="home-button-title">Obras</div>\n'
    '        <div class="home-button-desc">Cadastrar e editar obras</div>\n'
    '      </div>\n'
    '\n'
    '      <!-- 8. Reuniões (Reserved) -->\n'
    '      <div class="home-button btn-reunioes disabled">\n'
    '        <div class="home-button-icon">🗓️</div>\n'
    '        <div class="home-button-title">Reuniões</div>\n'
    '        <div class="home-button-desc">Em desenvolvimento</div>\n'
    '        <div class="home-button-badge">Em breve</div>\n'
    '      </div>\n'
    '\n'
    '      <!-- 9. Resumo do Tempo (Reserved) -->\n'
    '      <div class="home-button btn-tempo disabled">\n'
    '        <div class="home-button-icon">🌦️</div>\n'
    '        <div class="home-button-title">Resumo do Tempo</div>\n'
    '        <div class="home-button-desc">Em desenvolvimento</div>\n'
    '        <div class="home-button-badge">Em breve</div>\n'
    '      </div>\n'
    '    </div>'
)

if new in content:
    print('Já estava aplicado — nada a fazer.')
elif old in content:
    content = content.replace(old, new, 1)
    alvo.write_text(content, encoding='utf-8')
    print(f'OK: mudança aplicada em {alvo}')
else:
    print('AVISO: trecho não encontrado (arquivo pode já estar diferente). Nada foi alterado.')
    sys.exit(1)
