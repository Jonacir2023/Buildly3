#!/usr/bin/env python3
"""Gera o Registro do cofre a partir do git — uma nota por dia de trabalho.

Existe para que nenhuma alteração do BUILDLy fique sem nota. O git já sabe
tudo o que mudou; o que faltava era isso virar nota legível no Obsidian, sem
depender de alguém lembrar de escrever.

Cada nota tem duas partes:

  - o texto escrito à mão (o porquê, o que se aprendeu), acima do marcador;
  - o bloco entre os marcadores registro:auto, que este script reescreve a
    cada execução a partir do git.

O que está fora dos marcadores nunca é tocado. Rodar duas vezes seguidas não
muda nada — é seguro rodar sempre.

Uso:
    python3 scripts/registro_obsidian.py            # atualiza tudo
    python3 scripts/registro_obsidian.py --dia 2026-08-26
"""
import argparse
import pathlib
import re
import subprocess
import sys
from collections import OrderedDict

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DESTINO = RAIZ / 'vault' / 'Registro'
ABRE = '<!-- registro:auto:início — este bloco é reescrito pelo script, não edite à mão -->'
FECHA = '<!-- registro:auto:fim -->'

MESES = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho',
         'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']


def git(*args):
    # core.quotepath=false: sem isso o git devolve "vault/Decis\303\265es/..."
    # em vez de "vault/Decisões/...", e a nota fica ilegível.
    return subprocess.run(['git', '-C', str(RAIZ), '-c', 'core.quotepath=false', *args],
                          capture_output=True, text=True, check=True).stdout


def commits():
    """Todos os commits, do mais antigo para o mais novo, agrupados por dia."""
    bruto = git('log', '--reverse', '--date=short',
                '--format=%x01%H%x02%h%x02%ad%x02%an%x02%P%x02%s%x02%b')
    por_dia = OrderedDict()
    for pedaco in bruto.split('\x01'):
        if not pedaco.strip():
            continue
        campos = pedaco.split('\x02')
        if len(campos) < 6:
            continue
        sha, curto, data, autor, pais, assunto = campos[:6]
        corpo = campos[6] if len(campos) > 6 else ''
        por_dia.setdefault(data, []).append({
            'sha': sha, 'curto': curto, 'autor': autor.strip(),
            'merge': len(pais.split()) > 1,
            'assunto': assunto.strip(), 'corpo': corpo.strip(),
        })
    return por_dia


def arquivos(sha):
    """Arquivos tocados por um commit, com as linhas somadas e removidas."""
    saida = git('show', '--numstat', '--format=', sha)
    linhas = []
    for ln in saida.splitlines():
        partes = ln.split('\t')
        if len(partes) != 3:
            continue
        mais, menos, caminho = partes
        linhas.append((caminho, mais, menos))
    return linhas


def data_extenso(iso):
    a, m, d = iso.split('-')
    return f'{int(d)} de {MESES[int(m) - 1]} de {a}'


def bloco_auto(dia, lista):
    L = [ABRE, '']
    L.append(f'> {len(lista)} alteração(ões) registrada(s) no git em {data_extenso(dia)}.')
    L.append('')
    for c in lista:
        if c['merge']:
            pr = re.search(r'#(\d+)', c['assunto'])
            alvo = f'PR #{pr.group(1)}' if pr else 'ramo'
            L.append(f"- `{c['curto']}` — **mesclado o {alvo}** para `main`. "
                     f"A partir daqui está publicado no GitHub Pages.")
            L.append('')
            continue

        L.append(f"### `{c['curto']}` — {c['assunto']}")
        L.append('')
        if c['corpo']:
            for par in c['corpo'].split('\n\n'):
                texto = ' '.join(l.strip() for l in par.splitlines() if l.strip())
                if texto and not texto.startswith('Co-Authored-By')  \
                         and not texto.startswith('Claude-Session'):
                    L.append(texto)
                    L.append('')

        toques = arquivos(c['sha'])
        if toques:
            L.append('| Arquivo | + | − |')
            L.append('|---|---:|---:|')
            for caminho, mais, menos in toques:
                L.append(f'| `{caminho}` | {mais} | {menos} |')
            L.append('')

    L.append(FECHA)
    return '\n'.join(L)


CABECALHO = """---
criado: {dia}
tags: [registro, buildly]
---

# Registro — {extenso}

<!-- Escreva aqui, com suas palavras, o que aconteceu neste dia e por quê:
     o que motivou a mudança, o que foi testado, o que ficou pendente.
     Este texto é preservado — o script só reescreve o bloco automático. -->

## Alterações

"""

RODAPE = """

---

- [[Registro/Índice do Registro]]
- [[Projetos/BUILDLy Premium]]
"""


def escrever(dia, lista):
    DESTINO.mkdir(parents=True, exist_ok=True)
    alvo = DESTINO / f'{dia}.md'
    novo = bloco_auto(dia, lista)

    if alvo.exists():
        atual = alvo.read_text(encoding='utf-8')
        if ABRE in atual and FECHA in atual:
            antes = atual.split(ABRE)[0]
            depois = atual.split(FECHA, 1)[1]
            saida = antes + novo + depois
        else:
            saida = atual.rstrip() + '\n\n' + novo + RODAPE
    else:
        saida = CABECALHO.format(dia=dia, extenso=data_extenso(dia)) + novo + RODAPE

    if alvo.exists() and alvo.read_text(encoding='utf-8') == saida:
        return False
    alvo.write_text(saida, encoding='utf-8')
    return True


INDICE = """---
tags: [índice, registro]
---

# Índice do Registro

Uma nota por dia em que o BUILDLy mudou. Nenhuma alteração fica sem registro:
o bloco de alterações de cada nota é gerado do próprio git por
`scripts/registro_obsidian.py`, então não depende de ninguém lembrar.

O texto acima do bloco automático é escrito à mão — é onde mora o porquê, que
o git não guarda.

| Dia | Alterações |
|---|---|
{linhas}

---

- [[Início]]
- [[Projetos/BUILDLy Premium]] — o histórico contado por marcos, não por dia
- [[Notas/Como manter este cofre]]

#índice
"""


def escrever_indice(por_dia):
    linhas = []
    for dia in sorted(por_dia, reverse=True):
        n = len(por_dia[dia])
        linhas.append(f'| [[Registro/{dia}]] | {n} |')
    alvo = DESTINO / 'Índice do Registro.md'
    saida = INDICE.format(linhas='\n'.join(linhas))
    if alvo.exists() and alvo.read_text(encoding='utf-8') == saida:
        return False
    alvo.write_text(saida, encoding='utf-8')
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dia', help='só este dia (AAAA-MM-DD)')
    args = ap.parse_args()

    por_dia = commits()
    if args.dia:
        if args.dia not in por_dia:
            sys.exit(f'nenhum commit em {args.dia}')
        por_dia = {args.dia: por_dia[args.dia]}

    mudou = 0
    for dia, lista in por_dia.items():
        if escrever(dia, lista):
            print(f'  ~ {dia}.md ({len(lista)} alterações)')
            mudou += 1
        else:
            print(f'  = {dia}.md')
    if escrever_indice(commits()):
        print('  ~ Índice do Registro.md')
        mudou += 1
    print(f'OK — {mudou} nota(s) atualizada(s)')


main()
