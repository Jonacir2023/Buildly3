#!/usr/bin/env python3
"""Integra o novo app de Ata de Reunião (reuniao.html) ao buildly-completo.html:
adiciona a página iframe e liga o botão "Reuniões" da Home (funciona seja qual
for a ordem em que você aplicou o patch homebotoes.zip antes deste)."""
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

# ------------------------------------------------------------------
# 1) Página com o iframe do reuniao.html
# ------------------------------------------------------------------
iframe_novo = (
    '<!-- REUNIÃO PAGE (Ata de Reunião) -->\n'
    '<div class="page" id="page-reuniao">\n'
    '  <iframe id="reuniao-iframe" src="reuniao.html" style="width:100%;height:calc(100vh - 140px);border:none;background:#f0ece7;display:block;margin:0;padding:0" frameborder="0" allow="geolocation; microphone; camera"></iframe>\n'
    '</div>\n'
    '\n'
    '<!-- OBRA PAGE (cadastro compartilhado entre todos os apps) -->'
)
if 'id="page-reuniao"' in content:
    ja_aplicadas += 1
else:
    old = '<!-- OBRA PAGE (cadastro compartilhado entre todos os apps) -->'
    if old in content:
        content = content.replace(old, iframe_novo, 1)
        aplicadas += 1
    else:
        print('AVISO: âncora da página Obra não encontrada — página do iframe não inserida.')

# ------------------------------------------------------------------
# 2) Botão "Reuniões" na Home
# ------------------------------------------------------------------
botao_ativo = (
    "      <!-- 8. Reuniões (Ata de Reunião) -->\n"
    "      <div class=\"home-button btn-reunioes\" onclick=\"switchTab('reuniao', this)\">\n"
    "        <div class=\"home-button-icon\">🗓️</div>\n"
    "        <div class=\"home-button-title\">Reuniões</div>\n"
    "        <div class=\"home-button-desc\">Atas de reunião</div>\n"
    "      </div>"
)

if "switchTab('reuniao'" in content:
    ja_aplicadas += 1
else:
    # Caso A: já existe o botão placeholder "Em breve" (do patch homebotoes.zip) — upgrade
    botao_placeholder = (
        "      <!-- 8. Reuniões (Reserved) -->\n"
        "      <div class=\"home-button btn-reunioes disabled\">\n"
        "        <div class=\"home-button-icon\">🗓️</div>\n"
        "        <div class=\"home-button-title\">Reuniões</div>\n"
        "        <div class=\"home-button-desc\">Em desenvolvimento</div>\n"
        "        <div class=\"home-button-badge\">Em breve</div>\n"
        "      </div>"
    )
    if botao_placeholder in content:
        content = content.replace(botao_placeholder, botao_ativo, 1)
        aplicadas += 1
    else:
        # Caso B: botão ainda não existe de forma alguma — insere logo após o botão Obras
        ancora_obras = (
            "      <div class=\"home-button btn-obras\" onclick=\"switchTab('obra', this)\">\n"
            "        <div class=\"home-button-icon\">🏢</div>\n"
            "        <div class=\"home-button-title\">Obras</div>\n"
            "        <div class=\"home-button-desc\">Cadastrar e editar obras</div>\n"
            "      </div>"
        )
        if ancora_obras in content:
            content = content.replace(ancora_obras, ancora_obras + "\n\n" + botao_ativo, 1)
            aplicadas += 1
        else:
            print('AVISO: não encontrei nem o botão placeholder nem o botão Obras — botão Reuniões não inserido. Adicione manualmente ou peça ajuda.')

alvo.write_text(content, encoding='utf-8')
print(f'OK: {aplicadas} mudança(s) aplicada(s), {ja_aplicadas} já estavam aplicadas em {alvo}')
print('Lembrete: copie também o arquivo reuniao.html para dentro de ~/Buildly3 (o aplicar.py já faz isso).')
