---
criado: 2026-08-21
tags: [nota, meta, processo]
---

# Como manter este cofre

Este cofre existe para uma coisa: **a próxima sessão do Claude não precisar redescobrir o que
esta já descobriu.** Ele só cumpre isso se for atualizado junto com o trabalho.

---

## A regra base: nenhuma alteração sem registro

**Toda e qualquer mudança do BUILDLy vira nota.** Não é filtrada por importância — commit feito,
entrada no [[Registro/Índice do Registro]].

Isso não depende de memória de ninguém. O bloco de alterações de cada nota diária é gerado do
próprio git:

```bash
python3 scripts/registro_obsidian.py
```

Uma nota por dia, em `Registro/AAAA-MM-DD.md`, com cada commit, cada arquivo tocado e as linhas
somadas e removidas. Idempotente — pode rodar sempre.

O que o git **não** sabe é o porquê: o que motivou a mudança, o que foi testado, o que ficou
pendente. Isso se escreve à mão, acima do marcador `<!-- registro:auto -->`, e o script preserva.

Se um dia o Registro divergir do git, o git está certo — é só rodar o script de novo.

Uma consequência a saber: o commit que grava o próprio Registro fica de fora dele — não dá para
registrar um commit antes de ele existir. A execução seguinte o inclui. Por isso a última linha
do Registro costuma estar um commit atrás, e isso não é erro.

---

## A segunda regra: as notas de conhecimento acompanham

O Registro conta *o que aconteceu, quando*. As notas de `Notas/`, `Decisões/` e
`Projetos/` contam *como o sistema é e por quê* — e essas precisam ser mantidas à mão.

Toda sessão que fizer trabalho relevante no Buildly3 atualiza as notas afetadas **no mesmo
trabalho, sem esperar ser pedido**. A regra está registrada no `CLAUDE.md` da raiz do
repositório, que o Claude lê automaticamente ao abrir uma sessão aqui — é isso que faz o
processo funcionar sem o usuário ter que lembrar.

Conta como trabalho relevante: PR aberto ou mesclado, decisão tomada, mudança no contrato do
backend, armadilha nova descoberta, teste do usuário que confirma ou desmente algo.

---

## O que atualizar, em cada caso

| Aconteceu | Atualize |
|---|---|
| **Qualquer commit** | `python3 scripts/registro_obsidian.py` + o porquê à mão |
| **Mudança em HTML** | `python3 tests/executar.py` + `scripts/verificar_sintaxe.py` antes de entregar |
| PR aberto / mesclado / fechado | "Histórico" e "Fila de desenvolvimento" em [[Projetos/BUILDLy Premium]] |
| Decisão tomada | Nota nova em `Decisões/` + link no histórico do projeto |
| Endpoint mudou | [[Notas/Contrato do Backend]] |
| Chave de `localStorage` nova ou mudada | [[Notas/Armazenamento Local]] |
| Erro que custou tempo / dado | [[Notas/Regras Operacionais Críticas]] — com o motivo real |
| Layout do shell ou dos apps mudou | [[Notas/Arquitetura do App]] |
| Usuário testou e confirmou/desmentiu algo | Onde estiver escrito, marcando o que virou fato |

---

## Como escrever

- **Registre o porquê, não só o quê.** O código já diz o que faz; ele não diz por que a
  alternativa óbvia foi descartada. Isso é o que se perde entre sessões.
- **Separe o verificado do suposto.** Se algo não foi testado contra o Google ou em celular
  real, diga isso na própria nota. Um fato falso aqui é pior que ausência de nota.
- **Uma decisão por arquivo** em `Decisões/`, nomeada `AAAA-MM-DD Assunto.md`, com contexto →
  alternativas → decisão → consequências → pendente.
- **Histórico do projeto: mais recente primeiro.** Item resolvido sai da fila; não vira lista
  infinita de coisa feita.
- Prefira link `[[wikilink]]` a repetir informação. Duplicada, ela diverge.

---

## O que não guardar aqui

- Dados operacionais da obra (efetivo, RDO, notas fiscais) — o lugar deles é a planilha.
- Cópia de código que já está versionado no repositório. Referencie o caminho.
- Chave de API, token, credencial — nunca, em nenhuma nota. `ANTHROPIC_API_KEY` mora nas
  Propriedades do Script.

---

## Relacionado

- [[Início]]
- [[Registro/Índice do Registro]]
- [[Projetos/BUILDLy Premium]]
