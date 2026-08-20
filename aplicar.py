#!/usr/bin/env python3
import pathlib
import shutil
import subprocess
import sys

pasta = pathlib.Path(__file__).resolve().parent
if (pasta / 'buildly-completo.html').exists():
    destino = pasta
elif (pasta.parent / 'buildly-completo.html').exists():
    destino = pasta.parent
else:
    destino = pathlib.Path.cwd()

for nome in ('medicoes.html', 'documentos.html', 'manutencao.html'):
    origem = pasta / nome
    if origem.exists() and origem.resolve() != (destino / nome).resolve():
        shutil.copy(origem, destino / nome)
        print(f'Copiado {nome} para {destino}')

r = subprocess.run([sys.executable, str(pasta / '05_tres_apps.py')], cwd=destino)
sys.exit(r.returncode)
