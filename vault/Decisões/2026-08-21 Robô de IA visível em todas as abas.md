---
data: 2026-08-21
status: decidido
tags: [decisão, ia, ui, layout]
---

# Robô de IA vira botão flutuante

**Status:** ✅ Decidido · **PR:** #3 (`claude/robo-flutuante`)

---

## Contexto

Pedido: o robô (🤖 Perguntar sobre os dados) devia aparecer em qualquer aba, para tirar dúvida
de onde o usuário estivesse. Na prática só aparecia na Home.

**Causa:** o botão morava dentro de `#main-hdr`, o cabeçalho da Home, e `switchTab()` esconde
esse cabeçalho em toda aba que não seja `home`:

```js
homeHeader.style.display = tab === 'home' ? 'block' : 'none';
```

---

## Alternativas

1. **Reexibir `#main-hdr` nas outras abas.** Não funciona: Pauta, Check-in e Obra têm cabeçalho
   próprio fixo (`z-index:101`), e os 7 apps em iframe também. **Nenhuma das 10 telas reserva
   espaço para o cabeçalho do shell** — reexibi-lo cobriria o cabeçalho de cada uma, ou o topo
   do iframe.
2. **Duplicar o botão no cabeçalho de cada tela.** Dez lugares para manter em sincronia, sendo
   que 7 são arquivos separados que também rodam standalone.
3. **Botão flutuante fixo**, por cima de tudo.

---

## Decisão

Alternativa 3. `.fab-ia-wrap` / `.fab-ia-btn`, canto inferior direito, dentro da mesma coluna
central do app (480px no mobile, 1100px no desktop, acompanhando o breakpoint que já existia).

Um único ponto de manutenção, nenhum layout de tela precisou mudar. O botão antigo saiu do
cabeçalho da Home (ficaria duplicado) e `.fab-ia-wrap` entrou na lista de elementos escondidos
na impressão.

---

## Consequências

- Vira precedente: **qualquer elemento que precise existir em todas as abas tem que ser
  flutuante**, não colocado num cabeçalho. Registrado em
  [[Notas/Regras Operacionais Críticas]].
- O `z-index` escolhido (150) fica acima do conteúdo e dos cabeçalhos (100/101) e abaixo dos
  modais (200) — de propósito: o modal do próprio robô precisa cobrir o botão.

---

## Pendente

Testar no celular real, incluindo as abas não verificadas localmente (Reunião, Resumo do Tempo,
Medição, Documentos, Manutenção — mesmo padrão de iframe das que foram testadas), e em desktop
≥900px.

---

## Relacionado

- [[Notas/Arquitetura do App]]
- [[Projetos/BUILDLy Premium]]
