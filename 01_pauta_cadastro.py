#!/usr/bin/env python3
"""Pauta: remove o botão Exportar (quebrado) e coloca no lugar dele o botão
da engrenagem Admin, renomeado para Cadastro. Remove também o botão Admin
duplicado do cabeçalho."""
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
    '      <div style="display:flex;align-items:center;gap:8px">\n'
    '        <div class="hdr-date" id="pauta-hdr-date"></div>\n'
    '        <button class="btn-admin" onclick="pautaOpenAdmin()">⚙️ Admin</button>\n'
    '      </div>\n'
    '    </div>\n'
    '  </header>\n'
    '  <nav class="tabs" style="top:70px">\n'
    '    <div class="tab active" onclick="pautaGoTab(\'envio\',this)">📤 Envio</div>\n'
    '    <div class="tab" onclick="pautaGoTab(\'listar\',this)">📋 Listar</div>\n'
    '    <div class="tab" onclick="pautaGoTab(\'exportar\',this)">🚀 Exportar</div>\n'
    '  </nav>'
)
new = (
    '      <div style="display:flex;align-items:center;gap:8px">\n'
    '        <div class="hdr-date" id="pauta-hdr-date"></div>\n'
    '      </div>\n'
    '    </div>\n'
    '  </header>\n'
    '  <nav class="tabs" style="top:70px">\n'
    '    <div class="tab active" onclick="pautaGoTab(\'envio\',this)">📤 Envio</div>\n'
    '    <div class="tab" onclick="pautaGoTab(\'listar\',this)">📋 Listar</div>\n'
    '    <div class="tab" onclick="pautaOpenAdmin()">⚙️ Cadastro</div>\n'
    '  </nav>'
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
