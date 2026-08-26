---
criado: 2026-08-25
tags: [decisão, rdo, dados]
status: decidido
---

# Um RDO por apontador no mesmo dia

**Data:** 25/08/2026 · **Status:** ✅ Decidido e no ar

---

## Problema

O histórico do RDO era indexado só pela data:

```js
history['2026-08-24'] = { ...o diário do dia... }
```

Com um apontador só isso bastava. Com dois na mesma obra, o segundo a salvar **substituía** o
RDO do primeiro sem aviso — perda silenciosa de documento contratual, exatamente o que a
regra 2 de [[Notas/Regras Operacionais Críticas]] proíbe.

---

## Decisão

A chave do histórico passou a ser composta: `data#apontador-em-slug`.

```js
chaveDiario('2026-08-24', 'Renan de Souza')  // '2026-08-24#renan-de-souza'
```

O slug remove acentos (NFD + descarte de diacríticos), baixa a caixa e troca o que não for
`a-z0-9` por hífen — para que "Renan de Souza" e "renan de souza" caiam na mesma chave, e não
gerem dois RDOs do mesmo homem.

Tudo que antes lia `history[data]` passou a ir por um punhado de funções:

| Função | Para quê |
|---|---|
| `chaveDiario(data, apontador)` | monta a chave |
| `dataDaChave(chave)` | extrai só a data (o que está antes do `#`) |
| `chavesDaData(data)` / `rdosDaData(data)` | todos os RDOs de um dia |
| `datasDoHistorico()` | datas únicas, para o calendário |
| `rdoParaEditar(data)` | qual RDO abrir — prefere o do apontador deste aparelho |

---

## Migração

`migrarHistoricoParaMultiRdo()` reindexa as chaves antigas lendo o `apontador` de dentro de cada
diário. Roda sozinha ao carregar (linha 2317) **e** nos três caminhos de restauração de backup —
senão restaurar um backup antigo devolveria o formato velho e desfaria a migração.

É idempotente: chave que já tem `#` não é tocada. Rodar duas vezes não faz nada.

---

## Consequência que já mordeu

Funções que recebiam uma **data** continuaram existindo ao lado de funções que recebem uma
**chave**, e as duas são strings. `copiarUltimoDiario` recebia uma data de `datasDoHistorico()`
e ainda fazia `history[origem]` — que agora nunca existe. Corrigido com `rdoParaEditar(origem)`.

**Ao mexer no histórico, confirme se a variável é data ou chave.** O tipo não avisa.

---

## Relacionado

- [[Decisões/2026-08-25 Sincronização entre aparelhos]] — a mesma chave é a unidade da mescla
- [[Notas/Armazenamento Local]]
- [[Notas/RDO — Regras do Módulo]]
