#!/usr/bin/env python3
"""Roda as suítes de teste do BUILDLy e devolve um resumo.

Cada suíte é um arquivo solto que abre o app num navegador sem tela e confere
uma regra que já custou caro alguma vez. Elas imprimem "FALHAS: nenhuma"
quando passam — é isso que este runner procura.

    python3 tests/executar.py            # tudo
    python3 tests/executar.py rdo        # só as que têm "rdo" no nome
"""
import os
import pathlib
import subprocess
import sys

AQUI = pathlib.Path(__file__).resolve().parent
URL = os.environ.get('BUILDLY_URL', 'http://localhost:8795')


def main():
    filtro = sys.argv[1] if len(sys.argv) > 1 else ''
    suites = sorted(p for p in AQUI.glob('test_*.py') if filtro in p.name)
    if not suites:
        sys.exit(f'nenhuma suíte casa com {filtro!r}')

    print(f'app em {URL}\n')
    ruins = []
    for s in suites:
        r = subprocess.run([sys.executable, str(s)], capture_output=True, text=True)
        saida = r.stdout.strip().splitlines()
        ultima = saida[-1] if saida else '(sem saída)'
        ok = r.returncode == 0 and ultima.endswith('nenhuma')
        print(f'  {"OK   " if ok else "FALHA"}  {s.name:<34} {ultima}')
        if not ok:
            ruins.append((s.name, r.stdout + r.stderr))

    print()
    if ruins:
        for nome, saida in ruins:
            print(f'\n===== {nome} =====\n{saida}')
        print(f'{len(ruins)} de {len(suites)} suíte(s) com falha.')
        sys.exit(1)
    print(f'{len(suites)} suíte(s), todas verdes.')


main()
