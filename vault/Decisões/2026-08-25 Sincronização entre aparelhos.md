---
criado: 2026-08-25
tags: [decisão, rdo, sincronização, dados]
status: decidido
---

# Sincronização entre aparelhos (RDO)

**Data:** 25/08/2026 · **Status:** ✅ No ar — **falta validar com dois celulares reais**

---

## Problema

O RDO era 100% local. O que um apontador lançava no celular dele não chegava ao celular do
outro, e o espelho na nuvem subia no máximo **1× por dia** — na prática, o trabalho de hoje só
apareceria no outro aparelho amanhã, se aparecesse.

---

## Decisão

Sincronização periódica a cada **3 minutos** (`SYNC_INTERVALO_MS`), mais botão manual
"🔄 Sincronizar com os outros aparelhos" na configuração. Cada ciclo **sobe antes de buscar**, e
o envio tem débito de 4 s para não disparar a cada tecla.

`backupNuvem(manual, forcar)` ganhou o terceiro estado: o espelho diário continua 1×/dia, mas a
sincronização passa `forcar = true`.

### A política de conflito

O princípio é único: **nunca sobrescrever sem critério**. Cada tipo de dado tem a sua regra.

| Dado | Regra |
|---|---|
| Cadastro | entra o que é novo por id; **nada é removido** — remover apagaria o que o outro aparelho ainda não enviou |
| Baixa / retorno | viaja à parte, vence o `statusEm` mais recente — senão um aparelho desatualizado desfaria uma baixa |
| Diários | chave nova entra; chave existente, vence o `atualizadoEm` mais recente |
| Seleções do dia (`efetivoDia_`, `equipDia_`, `vlDia_`, `ativDia_`) | só entram junto de um diário **novo** aqui, e nunca por cima de uma chave que já existe localmente |

Isso só funciona porque o diário virou `data#apontador`
([[Decisões/2026-08-25 Um RDO por apontador no mesmo dia]]): dois apontadores no mesmo dia são
duas chaves diferentes e não competem. Competição de verdade só existe quando é **o mesmo
apontador em dois aparelhos** — e aí o carimbo mais recente é a resposta certa.

### Carimbos

`carimbar(obj)` grava `atualizadoEm` (ISO) e `atualizadoPor` (id do aparelho, sorteado uma vez e
guardado em `diario_obras_aparelho_id`).

`mesmoConteudoDiario(a, b)` compara **ignorando os carimbos**: um RDO idêntico vindo do outro
celular não é conflito, não regrava e não avisa. Sem isso, cada ciclo de 3 minutos anunciaria
"1 atualizado" para sempre.

`_mesclando` trava reentrância — a mescla chama `saveState`/`saveHistory`, que disparariam envio.

---

## O que ainda não foi provado

Tudo acima foi testado em navegador headless, simulando o outro aparelho. **Nenhum teste tocou o
Google.** Só dois celulares reais, na mesma obra, validam isto de ponta a ponta — e é o teste que
importa, porque envolve o Apps Script implantado, a pasta do Drive e a rede da obra.

---

## Relacionado

- [[Notas/Contrato do Backend]]
- [[Notas/Regras Operacionais Críticas]]
- [[Notas/RDO — Regras do Módulo]]
