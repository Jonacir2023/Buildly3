---
criado: 2026-08-25
tags: [decisão, rdo, dados]
status: decidido
---

# Baixa lógica no cadastro do RDO

**Data:** 25/08/2026 · **Status:** ✅ Decidido e no ar

---

## Problema

Remover um item do cadastro (veículo, equipamento, atividade, colaborador, categoria) apagava o
registro do array. O RDO de ontem que citava aquele item passava a apontar para um id que não
existe mais — e o documento de ontem mudava por causa de um cadastro de hoje.

O caso concreto: o Fusca sai da frota hoje. Editando o RDO de ontem, o Fusca sumia das opções,
como se não tivesse rodado. Documento contratual não pode ser reescrito para trás.

---

## Decisão

Nada é apagado do cadastro. A remoção vira **baixa**, com data:

```js
function baixarDoCadastro(item) {
  item.inativo = true;
  item.inativoEm = todayISO();          // dia em que saiu
  item.statusEm = new Date().toISOString();  // carimbo para a mescla entre aparelhos
}
```

E a exibição passa a depender do dia que está sendo editado:

```js
function itemVigenteNoDia(item, dia, usado) {
  if (usado) return true;               // foi lançado naquele dia: aparece sempre
  if (!item || !item.inativo) return true;
  if (!dia || !item.inativoEm) return false;
  return String(dia) < String(item.inativoEm);   // existia antes da baixa
}
```

Três consequências que valem por si:

- **`usado` vence tudo.** Se o item está marcado no RDO daquele dia, ele aparece mesmo depois da
  baixa — senão o próprio lançamento ficaria órfão.
- **Item com baixa não entra como "parado".** A lista de veículos parados é "vigentes do dia menos
  os que rodaram"; sem o filtro de vigência, o Fusca apareceria parado para sempre.
- **`categoriasVigentes()` devolve cópias.** É lista e soma, nunca escrita — devolver o objeto
  original convidava a mutação acidental de um cadastro filtrado.

## Recadastro reativa, não duplica

`reativarSeJaExiste(lista, casa)` procura o item com baixa pelo mesmo identificador natural
(placa, número) e o reativa, **mantendo o mesmo id**. Cadastrar de novo o Fusca não cria um
segundo Fusca — e os RDOs antigos continuam apontando certo.

## O usuário enxerga o que saiu

Cada lista de cadastro ganhou um bloco recolhido **"🗑️ Removidos (N)"** com botão de restaurar.
Baixa sem visibilidade vira dado perdido do ponto de vista de quem usa.

---

## Relacionado

- [[Notas/Regras Operacionais Críticas]]
- [[Decisões/2026-08-25 Sincronização entre aparelhos]] — baixa e retorno viajam por `statusEm`
- [[Notas/RDO — Regras do Módulo]]
