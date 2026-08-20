#!/usr/bin/env python3
"""Faz o robo (botao 🤖) enxergar tambem Medicoes, Documentos e Mural, que
so existem no navegador. E SO LEITURA: nenhum dado e alterado ou apagado."""
import json
import pathlib
import sys

pasta = pathlib.Path(__file__).resolve().parent
alvo = pasta / 'buildly-completo.html'
if not alvo.exists():
    alvo = pasta.parent / 'buildly-completo.html'
if not alvo.exists():
    alvo = pathlib.Path.cwd() / 'buildly-completo.html'
if not alvo.exists():
    print('ERRO: buildly-completo.html nao encontrado'); sys.exit(1)

TRECHOS = json.loads((pasta / 'trechos.json').read_text(encoding='utf-8'))

content = alvo.read_text(encoding='utf-8')
aplicadas = 0
ja_aplicadas = 0

for nome, (old, new) in TRECHOS.items():
    if new in content:
        ja_aplicadas += 1
    elif old in content:
        content = content.replace(old, new, 1)
        aplicadas += 1
    else:
        print(f'AVISO: trecho "{nome}" nao encontrado. Pulando.')

alvo.write_text(content, encoding='utf-8')
print(f'OK: {aplicadas} mudanca(s) aplicada(s), {ja_aplicadas} ja estavam aplicadas em {alvo}')
