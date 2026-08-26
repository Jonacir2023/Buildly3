---
criado: 2026-08-26
tags: [decisão, dados, localstorage]
status: decidido
---

# Espaço próprio de armazenamento

**Data:** 26/08/2026 · **Status:** ✅ No ar no repositório — falta publicar

---

## Problema

O usuário viu obra do diário de obras aparecendo dentro do BUILDLy e perguntou se os projetos
estavam sendo misturados. Os repositórios estão separados e o código de um não conhece o outro —
a mistura era do **navegador**.

`localStorage` é isolado por **origem**, não por pasta. Todos os apps do usuário são publicados
sob `https://jonacir2023.github.io`, e todos usavam as mesmas chaves
(`diario_obras_v4_state`, `diario_obras_v4_history_<obra>`, `pauta_*`, `chk_*`, `config`,
`obra_atual`…). Mesma origem + mesma chave = **um único pote compartilhado**.

Levantamento do dia: **17 chaves ou prefixos** colidiam entre os dois conjuntos de apps.

---

## Decisão

O BUILDLy passa a ter espaço fechado. Um bloco no topo de cada HTML troca `window.localStorage`
por uma versão que prefixa tudo com `buildly3::`:

```js
getItem: function (k) { return real.getItem(P + k); }
```

O app continua chamando `localStorage` como sempre — a tradução é invisível. `length` e `key(i)`
enxergam só o que é do BUILDLy, e `clear()` apaga só o que é do BUILDLy.

**Sem ponte, sem importação, sem pergunta.** O BUILDLy não lê nada de fora do próprio espaço, e
não apaga nada que não seja seu. São projetos diferentes e não se ligam.

## Por que um bloco, e não renomear as chaves

Renomear ~40 literais em 11 arquivos deixaria de fora o que é montado em tempo de execução
(`efetivoDia_${dia}`) e qualquer chave esquecida. O bloco fecha o espaço inteiro de uma vez:
nada escapa, nem por engano futuro.

## Consequência

Um aparelho que tenha RDO do BUILDLy no pote antigo (via `buildly2`) abre este app **vazio**.
Isso é correto e proposital — o caminho para trazer o histórico é a restauração do backup na
nuvem, que é dado do próprio BUILDLy, e não o pote compartilhado com outro app.

Como este repositório nunca foi publicado, ninguém tem dado sob o prefixo novo hoje. É a única
hora em que a separação sai sem migração no celular de ninguém.

---

## Relacionado

- [[Notas/Armazenamento Local]]
- [[Notas/Regras Operacionais Críticas]]
