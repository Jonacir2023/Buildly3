#!/usr/bin/env python3
"""Confere se o JavaScript embutido em cada HTML do app compila.

O projeto não tem build: um erro de sintaxe não aparece em lugar nenhum até
alguém abrir a página no celular e encontrar a tela morta. Este é o mais
próximo de um linter que faz sentido aqui — roda em segundos e pega a classe
de erro que mais dói.

Precisa do node apenas para `node --check`.
"""
import pathlib
import re
import subprocess
import sys
import tempfile

RAIZ = pathlib.Path(__file__).resolve().parent.parent


def main():
    problemas = []
    checados = 0
    for arq in sorted(RAIZ.glob('*.html')):
        texto = arq.read_text(encoding='utf-8', errors='ignore')
        # só scripts embutidos e sem type= exótico (JSON, template, módulo)
        for i, m in enumerate(re.finditer(r'<script(?![^>]*\ssrc=)([^>]*)>(.*?)</script>',
                                          texto, re.S | re.I)):
            atributos, corpo = m.group(1), m.group(2)
            if 'type=' in atributos.lower() and 'javascript' not in atributos.lower():
                continue
            if not corpo.strip():
                continue
            checados += 1
            with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False,
                                             encoding='utf-8') as f:
                f.write(corpo)
                tmp = f.name
            r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
            pathlib.Path(tmp).unlink()
            if r.returncode != 0:
                erro = (r.stderr.strip().splitlines() or ['erro desconhecido'])
                detalhe = next((l for l in erro if 'SyntaxError' in l), erro[-1])
                problemas.append(f'{arq.name} (script #{i + 1}): {detalhe}')

    for p in problemas:
        print(f'  FALHA   {p}')
    if problemas:
        print(f'\n{len(problemas)} script(s) com erro de sintaxe.')
        sys.exit(1)
    print(f'OK — {checados} bloco(s) de script conferido(s), nenhum erro de sintaxe.')


main()
