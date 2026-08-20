#!/usr/bin/env python3
"""Faz o app se adaptar ao tamanho da tela: no celular continua a coluna
estreita de sempre; no computador ocupa a largura da tela.

Esta versao tambem CORRIGE a anterior, que deixava os apps abertos em
iframe (RDO, Medicoes, Documentos, Manutencao, Reunioes, Resumo do Tempo
e Custos) ainda no formato de celular. Se voce ja aplicou a versao antiga,
o bloco antigo e substituido pelo novo — nao duplica.

E SO CSS. Nenhum dado e tocado e nenhuma linha de programacao e alterada:
tudo fica dentro de um @media que o navegador do celular nem le."""
import json
import pathlib
import sys

pasta = pathlib.Path(__file__).resolve().parent
if (pasta / 'buildly-completo.html').exists():
    destino = pasta
elif (pasta.parent / 'buildly-completo.html').exists():
    destino = pasta.parent
else:
    destino = pathlib.Path.cwd()

blocos = json.loads((pasta / 'blocos.json').read_text(encoding='utf-8'))

MARCA = 'DESKTOP — acima de 900px'   # presente na versao antiga e na nova
MARCA_860 = '860 e nao 900'          # so na versao nova dos sub-apps

novos = 0
atualizados = 0
ja_ok = 0
faltando = []

for nome, css in blocos.items():
    alvo = destino / nome
    if not alvo.exists():
        faltando.append(nome)
        continue

    txt = alvo.read_text(encoding='utf-8')

    if css in txt:
        ja_ok += 1
        continue

    if '</style>' not in txt:
        print(f'AVISO: {nome} nao tem bloco <style>. Pulando.')
        continue

    tinha_antigo = MARCA in txt
    if tinha_antigo:
        # Recorta o bloco anterior inteiro: do comentario de abertura ate
        # o </style> que vem logo depois dele.
        idx = txt.index(MARCA)
        ini = txt.rindex('/*', 0, idx)
        if MARCA_860 in txt:
            i860 = txt.index(MARCA_860)
            ini = min(ini, txt.rindex('/*', 0, i860))
        # Recua UMA quebra de linha (a linha em branco que separa o bloco
        # do CSS anterior). O bloco novo ja traz essa quebra de volta, entao
        # recuar mais de uma comeria a quebra da regra anterior.
        if ini > 0 and txt[ini - 1] == '\n':
            ini -= 1
        fim = txt.index('</style>', idx)
        txt = txt[:ini] + txt[fim:]

    i = txt.rindex('</style>')
    alvo.write_text(txt[:i] + css + txt[i:], encoding='utf-8')
    if tinha_antigo:
        atualizados += 1
    else:
        novos += 1

print(f'OK: {novos} arquivo(s) novo(s), {atualizados} corrigido(s) da versao anterior, {ja_ok} ja estavam certo(s)')
if faltando:
    print('Nao encontrados nesta pasta (ok se voce nao usa esses apps): ' + ', '.join(faltando))
