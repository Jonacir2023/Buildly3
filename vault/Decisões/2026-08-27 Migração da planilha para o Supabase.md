---
criado: 2026-08-27
atualizado: 2026-08-28
tags: [decisão, supabase, descartada]
status: superada
---

# Migração da planilha para o Supabase — DESCARTADA

**Status:** ❌ Superada em 28/08. O esquema foi removido deste repositório.

---

## O que se decidiu em 27/08

Levar os dados da planilha para o Supabase, com um esquema de 11 tabelas espelhando as abas
(`rdo`, `pauta`, `checkin`, `nota_fiscal`, `item_nf`) mais o cadastro. Escrito, testado num
PostgreSQL local e mesclado neste repositório.

## Por que foi descartado

No dia seguinte apareceu o **P3** — um projeto Supabase próprio, com modelagem que segue o
caminho oposto e certo: **não espelhar planilha.** Lá `pessoas` é separado de `contratos`,
o RDO tem tabelas filhas em vez de listas dentro de uma célula, e regra de negócio mora no
banco. Espelho de planilha gera tabela sem integridade e retrabalho garantido — o esquema
daqui tinha exatamente esse defeito.

Manter os dois seria a mesma armadilha que já custou caro neste projeto: dois esquemas
parecidos, em lugares diferentes, para o mesmo dado. Removidos deste repositório:

- `supabase/migrations/0001_esquema.sql` e `0002_rls.sql`
- `supabase/README.md`
- `scripts/planilha_para_supabase.py`

## Onde o assunto vive agora

**Fora daqui, e é assim que tem de ser.** O P3 é projeto separado, com repositório e banco
próprios. Este repositório volta a ser só o BUILDLy: HTML estático, Apps Script e planilha.

O que sobreviveu foi o aprendizado, não o código — está em
[[Decisões/2026-08-26 Isolamento definitivo entre projetos]].
