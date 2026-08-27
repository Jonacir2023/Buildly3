#!/usr/bin/env python3
"""Converte os CSV exportados da planilha em SQL de inserção para o Supabase.

Princípio: **não inventar dado.** Coluna que o script não reconhece, linha que
não bate com o esperado, data em formato estranho — tudo é reportado, nada é
adivinhado. Um RDO é documento contratual; palpite aqui vira erro de obra.

Uso:
    python3 scripts/planilha_para_supabase.py \\
        --diario 'Diário.csv' --pauta Pauta.csv --checkin CheckIn.csv \\
        --nf 'Notas Fiscais.csv' --itens 'Itens NF.csv' \\
        --obra-id 11111111-1111-1111-1111-111111111111 \\
        --saida supabase/import.sql

Todos os arquivos são opcionais: converte o que receber.
"""
import argparse
import csv
import pathlib
import re
import sys
import unicodedata

# --------------------------------------------------------------------------
# Mapa cabeçalho-da-planilha → coluna-do-banco. As chaves são comparadas já
# normalizadas (sem acento, minúsculas, só letras e números), do mesmo jeito
# que o Apps Script compara — é o que faz 'Descrição do Local' casar mesmo se
# alguém tiver digitado 'Descricao do local'.
# --------------------------------------------------------------------------
MAPAS = {
    'rdo': {
        'data': 'data', 'diadasemana': 'dia_semana',
        'localdaobra': 'local_obra', 'descricaodolocal': 'descricao_local',
        'tempoclima': 'tempo_clima', 'jornada': 'jornada',
        'dsshorario': 'dss_horario', 'dssministradopor': 'dss_ministrado_por',
        'dsstema': 'dss_tema', 'atividadesdodia': 'atividades_do_dia',
        'efetivototal': 'efetivo_total', 'efetivoporfuncao': 'efetivo_por_funcao',
        'colaboradorespresentes': 'colaboradores_presentes',
        'equipamentosutilizados': 'equipamentos_utilizados',
        'veiculosleves': 'veiculos_leves',
        'veiculosequipparados': 'veiculos_equip_parados',
        'eventosdeseguranca': 'eventos_seguranca',
        'eventosdemeioambiente': 'eventos_meio_ambiente',
        'observacoesdodia': 'observacoes_do_dia',
        'apontador': 'apontador', 'fotos': 'fotos', 'rdon': 'rdo_numero',
        # Obra/Empresa/Cidade não viram coluna do RDO: identificam a obra.
        'obra': None, 'empresa': None, 'cidade': None,
    },
    'pauta': {
        'id': 'id', 'assunto': 'assunto', 'descricao': 'descricao',
        'criador': 'criador', 'responsavel': 'responsavel', 'setor': 'setor',
        'prioridade': 'prioridade', 'status': 'status',
        'datalancamento': 'data_lancamento', 'datadelancamento': 'data_lancamento',
        'datatermino': 'data_termino', 'datadetermino': 'data_termino',
        'criadoem': 'criado_em', 'atualizadoem': 'atualizado_em',
    },
    'checkin': {
        'id': 'id', 'assunto': 'assunto', 'descricao': 'descricao',
        'criador': 'criador', 'responsavel': 'responsavel', 'setor': 'setor',
        'prioridade': 'prioridade', 'status': 'status',
        'datatermino': 'data_termino', 'concluidoem': 'concluido_em',
        'criadoem': 'criado_em', 'atualizadoem': 'atualizado_em',
    },
    'nota_fiscal': {
        'id': 'id', 'numeronf': 'numero_nf', 'serie': 'serie',
        'dataemissao': 'data_emissao', 'fornecedor': 'fornecedor',
        'categoria': 'categoria', 'responsavel': 'responsavel',
        'observacoes': 'observacoes', 'totalnf': 'total_nf', 'criadoem': 'criado_em',
    },
    'item_nf': {
        'iditem': 'id', 'idnf': 'nota_fiscal_id', 'numeronf': 'numero_nf',
        'descricao': 'descricao', 'quantidade': 'quantidade',
        'precounitario': 'preco_unitario', 'total': 'total',
    },
}

# Colunas sem as quais a linha não entra. Emitir SQL que o banco vai recusar é
# pior que recusar aqui: no meio de uma transação, uma linha ruim derruba a
# importação inteira e ninguém sabe quantas já tinham entrado.
OBRIGATORIAS = {
    'rdo': ['data', 'apontador'],
    'pauta': ['id', 'assunto'],
    'checkin': ['id', 'assunto'],
    'nota_fiscal': ['id'],
    'item_nf': ['id', 'nota_fiscal_id'],
}

DATAS = {'data', 'data_lancamento', 'data_termino', 'data_emissao'}
NUMEROS = {'efetivo_total', 'total_nf', 'quantidade', 'preco_unitario', 'total'}

problemas = []


def norm(s):
    s = unicodedata.normalize('NFD', str(s or ''))
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]', '', s.lower())


def sql_texto(v):
    return "'" + str(v).replace("'", "''") + "'"


def sql_data(v, onde):
    """Aceita AAAA-MM-DD e DD/MM/AAAA. Qualquer outra coisa vira NULL e é
    reportada — data errada num RDO é pior que data ausente."""
    v = str(v or '').strip()
    if not v:
        return 'null'
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', v):
        return sql_texto(v)
    m = re.fullmatch(r'(\d{1,2})/(\d{1,2})/(\d{4})', v)
    if m:
        d, mes, a = m.groups()
        return sql_texto(f'{a}-{int(mes):02d}-{int(d):02d}')
    problemas.append(f'{onde}: data em formato não reconhecido ({v!r}) — foi para NULL')
    return 'null'


def sql_numero(v, onde):
    v = str(v or '').strip().replace('R$', '').replace(' ', '')
    if not v:
        return 'null'
    # 1.234,56 (planilha em pt-BR) → 1234.56
    if re.fullmatch(r'-?\d{1,3}(\.\d{3})*(,\d+)?', v):
        v = v.replace('.', '').replace(',', '.')
    else:
        v = v.replace(',', '.')
    try:
        float(v)
        return v
    except ValueError:
        problemas.append(f'{onde}: número não reconhecido ({v!r}) — foi para NULL')
        return 'null'


def converter(caminho, tabela, extras=None):
    mapa = MAPAS[tabela]
    linhas_sql = []
    with open(caminho, newline='', encoding='utf-8-sig') as f:
        leitor = csv.DictReader(f)
        if not leitor.fieldnames:
            problemas.append(f'{caminho}: arquivo sem cabeçalho')
            return []

        colunas, desconhecidas = {}, []
        for h in leitor.fieldnames:
            n = norm(h)
            if n in mapa:
                if mapa[n]:
                    colunas[h] = mapa[n]
            elif n:
                desconhecidas.append(h)
        for h in desconhecidas:
            problemas.append(f'{caminho}: coluna "{h}" não existe no banco — ignorada')
        esperadas = {v for v in mapa.values() if v}
        faltando = esperadas - set(colunas.values())
        for c in sorted(faltando):
            problemas.append(f'{caminho}: o banco tem "{c}" e a planilha não trouxe — ficará no padrão')

        for i, linha in enumerate(leitor, start=2):
            if not any(str(v or '').strip() for v in linha.values()):
                continue
            campos, valores = [], []
            for h, col in colunas.items():
                bruto = linha.get(h)
                onde = f'{caminho} linha {i}, "{h}"'
                if col in DATAS:
                    valores.append(sql_data(bruto, onde))
                elif col in NUMEROS:
                    valores.append(sql_numero(bruto, onde))
                else:
                    valores.append(sql_texto(str(bruto or '').strip()))
                campos.append(col)
            for col, val in (extras or {}).items():
                campos.append(col); valores.append(val)

            faltou = []
            for col in OBRIGATORIAS.get(tabela, []):
                if col not in campos:
                    faltou.append(col)
                    continue
                v = valores[campos.index(col)]
                if v in ('null', "''"):
                    faltou.append(col)
            if faltou:
                problemas.append(
                    f'{caminho} linha {i}: sem {", ".join(faltou)} — a linha não entra. '
                    'Precisa de decisão sua; não vou adivinhar.')
                continue

            linhas_sql.append(
                f'insert into {tabela} ({", ".join(campos)}) values ({", ".join(valores)});')
    return linhas_sql


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--diario'); ap.add_argument('--pauta'); ap.add_argument('--checkin')
    ap.add_argument('--nf'); ap.add_argument('--itens')
    ap.add_argument('--obra-id', help='uuid da obra a que os RDOs pertencem')
    ap.add_argument('--saida', default='supabase/import.sql')
    a = ap.parse_args()

    saida = ['-- Gerado por scripts/planilha_para_supabase.py — confira antes de aplicar.',
             'begin;']
    total = 0
    for caminho, tabela, extras in [
        (a.diario, 'rdo', {'obra_id': sql_texto(a.obra_id)} if a.obra_id else None),
        (a.pauta, 'pauta', None), (a.checkin, 'checkin', None),
        (a.nf, 'nota_fiscal', None), (a.itens, 'item_nf', None),
    ]:
        if not caminho:
            continue
        if tabela == 'rdo' and not a.obra_id:
            sys.exit('--diario exige --obra-id: o RDO precisa saber a que obra pertence')
        linhas = converter(caminho, tabela, extras)
        saida.append(f'\n-- {tabela}: {len(linhas)} linha(s) de {caminho}')
        saida.extend(linhas)
        total += len(linhas)
        print(f'  {tabela:<12} {len(linhas):>5} linha(s)')

    saida.append('\ncommit;')
    pathlib.Path(a.saida).write_text('\n'.join(saida) + '\n', encoding='utf-8')

    print()
    for p in problemas:
        print(f'  ATENÇÃO  {p}')
    print(f'\n{total} inserção(ões) em {a.saida}'
          f'{" — " + str(len(problemas)) + " ponto(s) a conferir" if problemas else ""}')
    if problemas:
        sys.exit(2)


main()
