#!/usr/bin/env python3
"""Corrige o Check-in: salvar a reuniao passa a gravar os status de verdade,
e o botao Atualizar nao desfaz mais o que foi registrado no dia."""
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

trechos = json.loads((pasta / 'trechos.json').read_text(encoding='utf-8'))

content = alvo.read_text(encoding='utf-8')
aplicadas = 0
ja_aplicadas = 0
falhas = []

for nome, (antigo, novo) in trechos.items():
    if novo in content:
        ja_aplicadas += 1
    elif antigo in content:
        content = content.replace(antigo, novo, 1)
        aplicadas += 1
    else:
        falhas.append(nome)

if falhas:
    print('AVISO: nao encontrei estes trechos (nada foi gravado): ' + ', '.join(falhas))
    if not aplicadas:
        sys.exit(1)

alvo.write_text(content, encoding='utf-8')
print(f'OK: {aplicadas} correcao(oes) aplicada(s), {ja_aplicadas} ja estavam aplicadas em {alvo}')
