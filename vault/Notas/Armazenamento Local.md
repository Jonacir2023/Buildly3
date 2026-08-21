---
criado: 2026-08-21
tags: [nota, localstorage, dados, frontend]
---

# Armazenamento Local (localStorage)

Todos os apps guardam estado no `localStorage` do navegador. Parte disso sobe para a planilha
(Pauta, Check-in, RDO); **parte existe só no aparelho** — e essa distinção é a origem de vários
problemas.

---

## Chaves por app

| App | Prefixo / chave | Sobe para a planilha? |
|---|---|---|
| Pauta | `pauta_*` (`pauta_assuntos`, …) | Sim |
| Check-in | `chk_*` (`chk_assuntos`, `chk_removidos`) | Sim |
| Custos | `custo_*` (`custo_notasfiscais`, …) | **Não** (endpoint existe, front-end não chama) |
| RDO | `diario_obras_v4_state`, `diario_obras_v4_history_<obra>` | Sim |
| Obra (compartilhado) | `b3_obra` | — |
| Medições | `med_contratos` | **Não** |
| Documentos | `doc_arquivos`, `doc_notas_manuais` | **Não** |
| Manutenção | `manut_mural`, `manut_ultimo_autor` | **Não** |
| Reunião | `reuniao_atas` | **Não** |

O que não sobe para a planilha é justamente o que o robô de IA recebe via `contextoLocal` na
pergunta — ver [[Notas/Contrato do Backend]].

---

## Armadilha: a chave do RDO carrega o nome da obra

```js
const HISTORY_KEY_BASE = 'diario_obras_v4_history';
// chave real: HISTORY_KEY_BASE + '_' + obra.nome.replace(/\s+/g,'_').toLowerCase()
```

Isolamento por obra é intencional (versão 20 do RDO), mas tem uma consequência que já confundiu:
**renomear a obra "esconde" todos os RDOs antigos**, porque o app passa a ler outra chave. Os
dados não foram perdidos — estão na chave do nome anterior, e a planilha continua intacta de
qualquer jeito (é ela a fonte de verdade). Se acontecer, restaure pelo backup na nuvem ou
volte o nome exato da obra.

Há também as chaves legadas `diario_obras_v3_state` / `_history`, lidas só para migração.

Chaves auxiliares por dia, incluídas no backup: `efetivoDia_`, `equipDia_`, `vlDia_`,
`ativDia_` (sufixo = data), mais `ultimoBackupNuvem` e `diario_obras_v3_autobackup`.

---

## Armadilha: cota estourada por foto em base64

Fotos guardadas como data URI dentro do `localStorage` consomem muito espaço e a cota estoura
sem aviso — o `setItem` lança exceção e, se ninguém tratar, **o registro que o usuário acabou
de preencher se perde em silêncio**.

Regra: onde o registro pode carregar imagem embutida (Custos, RDO), envolva a gravação em
`try/catch` e avise o usuário em vez de deixar falhar quieto. Ver
[[Decisões/2026-08-21 Escaneamento de nota fiscal]].

---

## Armadilha: PWA e navegação privada no iOS

Herdada do app antigo, e a causa mais provável da perda recorrente de dados que já aconteceu
lá: reinstalar o ícone PWA na tela de início do iPhone pode criar um container de
`localStorage` separado e zerado. O Safari em modo privado também isola/descarta o
armazenamento entre sessões.

Por isso: **a planilha é a fonte de verdade, o local é cache.** Se o app abrir vazio, restaure
da nuvem — nunca peça para o usuário redigitar cadastro.

---

## Relacionado

- [[Notas/Regras Operacionais Críticas]]
- [[Notas/Arquitetura do App]]
- [[Notas/Contrato do Backend]]
