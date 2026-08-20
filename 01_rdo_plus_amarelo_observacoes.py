#!/usr/bin/env python3
"""RDO/Diario: colore todos os sinais de + (adicionar item) em amarelo, e
troca o separador das Observacoes do Dia de '.-' para '*' (cada trecho
separado por * vira uma linha/bullet no PDF e no texto do WhatsApp)."""
import pathlib
import sys

pasta = pathlib.Path(__file__).resolve().parent
alvo = pasta / 'rdo.html'
if not alvo.exists():
    alvo = pasta.parent / 'rdo.html'
if not alvo.exists():
    alvo = pathlib.Path.cwd() / 'rdo.html'
if not alvo.exists():
    print('ERRO: rdo.html não encontrado'); sys.exit(1)

content = alvo.read_text(encoding='utf-8')
aplicadas = 0
ja_aplicadas = 0


def aplicar(old, new, nome, count=1):
    global content, aplicadas, ja_aplicadas
    if new in content and old not in content:
        ja_aplicadas += 1
        return
    n = content.count(old)
    if n == 0:
        print(f'AVISO: trecho "{nome}" não encontrado. Pulando.')
        return
    if count is not None and n != count:
        print(f'AVISO: trecho "{nome}" esperava {count} ocorrência(s), achei {n}. Aplicando mesmo assim.')
    content = content.replace(old, new)
    aplicadas += 1


# 1) Botões-ícone com o emoji ➕ (7 ocorrências) -> "+" estilizado em amarelo
aplicar(
    '>➕</button>',
    '><span style="color:var(--accent-soft);font-weight:800;font-size:18px;line-height:1">+</span></button>',
    'icone-mais-emoji',
    count=7,
)

# 2) Botões "+ Adicionar atividade paralisada"
aplicar(
    '<button class="add-btn-full" onclick="abrirModalAtivParalisada()">+ Adicionar atividade paralisada</button>',
    '<button class="add-btn-full" onclick="abrirModalAtivParalisada()"><span style="color:var(--accent-soft)">+</span> Adicionar atividade paralisada</button>',
    'btn-ativ-paralisada',
)

# 3) "+ Registrar evento avulso" (2 ocorrências: seguranca e meio ambiente)
aplicar(
    '>+ Registrar evento avulso<',
    '><span style="color:var(--accent-soft)">+</span> Registrar evento avulso<',
    'btn-evento-avulso',
    count=2,
)

# 4) "+ Adicionar Categoria"
aplicar(
    '<button class="add-btn-full" onclick="abrirModalCategoria()">+ Adicionar Categoria</button>',
    '<button class="add-btn-full" onclick="abrirModalCategoria()"><span style="color:var(--accent-soft)">+</span> Adicionar Categoria</button>',
    'btn-categoria',
)

# 5) "+ Adicionar Equipamento"
aplicar(
    '<button class="add-btn-full" onclick="abrirModalEquipamento()">+ Adicionar Equipamento</button>',
    '<button class="add-btn-full" onclick="abrirModalEquipamento()"><span style="color:var(--accent-soft)">+</span> Adicionar Equipamento</button>',
    'btn-equipamento',
)

# 6) "+ Adicionar Veículo Leve"
aplicar(
    '<button class="add-btn-full" onclick="abrirModalVeiculoFrota()">+ Adicionar Veículo Leve</button>',
    '<button class="add-btn-full" onclick="abrirModalVeiculoFrota()"><span style="color:var(--accent-soft)">+</span> Adicionar Veículo Leve</button>',
    'btn-veiculo-leve',
)

# 7) "+ Adicionar Atividade Padrão"
aplicar(
    '<button class="add-btn-full" onclick="abrirModalAtividade()">+ Adicionar Atividade Padrão</button>',
    '<button class="add-btn-full" onclick="abrirModalAtividade()"><span style="color:var(--accent-soft)">+</span> Adicionar Atividade Padrão</button>',
    'btn-atividade-padrao',
)

# 8) "+ Adicionar Tipo" (2 ocorrências: seguranca e meio ambiente)
aplicar(
    '>+ Adicionar Tipo<',
    '><span style="color:var(--accent-soft)">+</span> Adicionar Tipo<',
    'btn-adicionar-tipo',
    count=2,
)

# 9) Botão gerado via JS "+ Colaborador"
aplicar(
    "    btnAdd.textContent = '+ Colaborador';",
    '    btnAdd.innerHTML = \'<span style="color:var(--accent-soft)">+</span> Colaborador\';',
    'btn-colaborador-js',
)

# 10) Placeholder das Observações do Dia — adiciona dica do separador *
aplicar(
    '<textarea id="observacoesDia" placeholder="Registre aqui informações importantes do dia: ocorrências, decisões, visitas, pendências, condições especiais..." style="min-height:140px;resize:vertical"></textarea>',
    '<textarea id="observacoesDia" placeholder="Registre aqui informações importantes do dia: ocorrências, decisões, visitas, pendências, condições especiais... Use * para separar cada observação em uma linha." style="min-height:140px;resize:vertical"></textarea>',
    'placeholder-observacoes',
)

# 11) PDF: separa observações por * (cada trecho vira uma linha)
aplicar(
    '        <div style="background: #fdfdfd; padding: 12px; border: 1px solid #dee2e6; border-radius: 4px; font-size: 9pt; min-height: 60px;">\n'
    '            ${escHtml(day.observacoesDia.trim())}\n'
    "        </div>` : ''}",
    '        <div style="background: #fdfdfd; padding: 12px; border: 1px solid #dee2e6; border-radius: 4px; font-size: 9pt; min-height: 60px;">\n'
    "            ${day.observacoesDia.split('*').map(s => s.trim()).filter(Boolean).map(escHtml).join('<br>')}\n"
    "        </div>` : ''}",
    'pdf-observacoes-split',
)

# 12) WhatsApp: separa observações por * (cada trecho vira um bullet)
aplicar(
    "  if (day.observacoesDia && day.observacoesDia.trim()) {\n"
    "    txt += `\\n${divisor}\\n\\n`;\n"
    "    txt += `*📝 Observações do Dia*\\n${day.observacoesDia.trim()}\\n`;\n"
    "  }",
    "  if (day.observacoesDia && day.observacoesDia.trim()) {\n"
    "    txt += `\\n${divisor}\\n\\n`;\n"
    "    txt += `*📝 Observações do Dia*\\n`;\n"
    "    day.observacoesDia.split('*').map(s => s.trim()).filter(Boolean).forEach(o => txt += `• ${o}\\n`);\n"
    "  }",
    'whatsapp-observacoes-split',
)

alvo.write_text(content, encoding='utf-8')
print(f'OK: {aplicadas} mudança(s) aplicada(s), {ja_aplicadas} já estavam aplicadas em {alvo}')
