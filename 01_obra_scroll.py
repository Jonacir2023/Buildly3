#!/usr/bin/env python3
"""Obras: cabecalho fixo no topo e area de conteudo com rolagem propria
(independente da rolagem das outras abas), respondendo ao scroll do mouse."""
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
        '  <div style="padding-top:86px;padding-left:16px;padding-right:16px">\n'
        '    <div class="sec">\n'
        '      <div class="sec-title">🏗️ Identificação</div>',
        '  <div id="obra-scroll-body" style="position:fixed;top:70px;left:50%;transform:translateX(-50%);width:100%;max-width:480px;bottom:0;overflow-y:auto;-webkit-overflow-scrolling:touch;padding:16px">\n'
        '    <div class="sec">\n'
        '      <div class="sec-title">🏗️ Identificação</div>',
        'obra-div-scroll',
    ),
    (
        'function obraInit() {\n'
        '  const o = obraCompartilhada();',
        'function obraInit() {\n'
        '  const scrollBody = document.getElementById(\'obra-scroll-body\');\n'
        '  if (scrollBody) scrollBody.scrollTop = 0;\n'
        '  const o = obraCompartilhada();',
        'obra-init-scrolltop',
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
