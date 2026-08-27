---
criado: 2026-08-27
tags: [decisão, supabase, dados, migração]
status: em andamento
---

# Migração da planilha para o Supabase

**Data:** 27/08/2026 · **Status:** 🟡 Esquema pronto e testado; nada aplicado

Decisão do usuário: levar os dados do Google Sheets para o Supabase, **mantendo as fotos no
Google Drive**.

---

## Não havia o que formatar

O pedido era "formate o Supabase". Fui olhar antes: a organização existe (plano gratuito) e tem
**zero projetos**. O `/app-supabase/` do repositório é código e migrações que nunca foram
aplicados a projeto nenhum. Nenhuma ação destrutiva foi necessária.

## Forma do esquema

Onze tabelas. As cinco primeiras espelham as abas da planilha; as outras seis são o cadastro,
que **nunca esteve na planilha** — vive só no `localStorage` de cada aparelho, e é por isso que
cada celular tem a sua lista e limpar o navegador apaga tudo. **É o maior ganho isolado desta
migração.**

Decisão de forma, e ela é deliberada: nesta etapa as listas do RDO (atividades do dia, efetivo
por função, equipamentos usados) continuam como **texto**, como a planilha guarda. Normalizar
agora obrigaria a reescrever o app no mesmo passo da migração de dados — dois riscos ao mesmo
tempo. Primeiro o dado chega inteiro e conferível; depois se normaliza o que ganhar algo com
isso.

As regras que o app já tem viraram regra do banco:

- `unique (obra_id, data, lower(apontador))` — um RDO por apontador por dia, agora garantido
  pelo banco e não pela boa vontade do código.
- `inativo` / `inativo_em` / `status_em` no cadastro — a baixa lógica.
- Trigger de `atualizado_em` — o carimbo que decide quem vence quando dois aparelhos editam.

A **obra ganhou identidade própria** (`uuid`), e o nome virou rótulo editável. Isso mata a
armadilha de renomear a obra e "perder" o histórico.

## Segurança não é detalhe aqui

O app é página estática, e nela a chave `anon` **é pública**. A única coisa entre o dado e a
internet são as políticas RLS. Nesta etapa: nada é legível sem login; quem está autenticado vê
tudo. Além disso o papel `anon` perde o próprio acesso às tabelas — assim, uma política
permissiva criada por engano no futuro ainda não abriria o banco.

## O que ainda falta, e é a maior parte

1. Criar o projeto (nome, região, senha — decisão do usuário)
2. Exportar as 5 abas em CSV — **só o usuário pode**, o ambiente do Claude não alcança o Google
3. Importar com `scripts/planilha_para_supabase.py`
4. **Reescrever a camada de dados do `rdo.html`** — 7.550 linhas hoje escritas contra
   `localStorage` + Apps Script. É aqui que mora o risco de perder o que foi construído nesta
   semana.

Nada disso desliga o `buildly2`. Ver
[[Decisões/2026-08-26 Isolamento definitivo entre projetos]].

---

## Relacionado

- [[Notas/Contrato do Backend]]
- [[Notas/Armazenamento Local]]
