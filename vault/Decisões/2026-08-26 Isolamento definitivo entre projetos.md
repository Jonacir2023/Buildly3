---
criado: 2026-08-26
tags: [decisão, isolamento, dados, crítico]
status: decidido
---

# Isolamento definitivo entre projetos

**Data:** 26/08/2026 · **Status:** ✅ Feito no código — falta a parte que só o usuário faz

---

## O incidente

O usuário alterou o efetivo no RDO do BUILDLy. O Renan relatou que a alteração apareceu no
diário de obras de **outro projeto**, em outro aparelho.

Outro aparelho descarta o navegador como causa: `localStorage` é local. A alteração viajou pelo
**backend**.

## A causa

Não são "dois apps parecidos que vazaram um no outro". O app publicado em `buildly2` **é** o
diário do outro projeto:

| | buildly2 (no ar) | o outro projeto |
|---|---|---|
| `rdo.html` | — | **byte a byte igual** |
| Apps Script | `AKfycbwa_TMG…` | `AKfycbwa_TMG…` — **o mesmo `/exec`** |
| Planilha | a que aquele script abre | a mesma |

Dois endereços, um app só. Editar o efetivo em `buildly2` **é** editar o diário do outro
projeto. Não havia nada a "vazar": era o mesmo sistema.

## Os três canais de contaminação

| Canal | Como contamina | Situação |
|---|---|---|
| Mesmo arquivo / mesmo código | o app publicado é literalmente o outro | Buildly3 já é outro arquivo ✅ |
| Mesmo `localStorage` | mesma origem + mesmas chaves, no mesmo aparelho | cortado com `buildly3::` ✅ |
| Mesmo backend | mesmo `/exec` → mesma planilha → **atravessa aparelhos** | Buildly3 tem `/exec` e planilha próprios ✅ |

O terceiro é o pior justamente por atravessar aparelhos: nenhuma correção no navegador o
alcança.

## O que foi feito

1. **Pastas do Drive com nome próprio** — `BUILDLy - Fotos` e `BUILDLy - Backups`. Antes eram
   `Diario de Obras - …`, genéricas: qualquer app do mesmo Drive cairia nas mesmas pastas.
2. **Apagado o código que escrevia na API de outro repositório.** Estava desligado por um
   `return`, mas o campo de token e a tela de status continuavam vivos — prometendo uma
   sincronização que não existia e pedindo credencial à toa.
3. **`scripts/verificar_isolamento.py`** — falha se encontrar qualquer vínculo: `/exec` que não
   seja o do BUILDLy, planilha que não seja a dele, endereço ou repositório de outro projeto,
   pasta de Drive com nome genérico, ou app sem o espaço próprio de `localStorage`.

## Por que um verificador, e não uma regra escrita

Regra escrita depende de alguém lembrar. Este incidente não veio de desatenção — veio de um
endereço publicado apontando para o backend errado, coisa que nenhuma leitura de código pega no
dia a dia. O verificador roda em segundos e **falha**; é o que impede a repetição.

## O que só o usuário pode fazer

**Tirar o `buildly2` do ar.** Enquanto aquele endereço existir, qualquer pessoa que o abrir
escreve no backend do outro projeto. Isso não é corrigível daqui: `buildly2` é outro
repositório. Publicar o Buildly3 não basta — é preciso despublicar o antigo.

---

## Relacionado

- [[Notas/Armazenamento Local]]
- [[Decisões/2026-08-26 Espaço próprio de armazenamento]]
- [[Notas/Regras Operacionais Críticas]]
