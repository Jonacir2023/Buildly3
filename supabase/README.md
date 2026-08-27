# Migração da planilha para o Supabase

Estado: **esquema escrito, nada aplicado.** Não existe projeto Supabase na conta
(a organização existe, no plano gratuito, com zero projetos) — não havia o que
formatar.

As **fotos continuam no Google Drive**. Aqui guardamos só os links, como a
planilha já fazia.

---

## O que precisa acontecer, em ordem

### 1. Criar o projeto Supabase
Precisa de decisão do usuário: nome, região e senha do banco. Nada disso é
adivinhável, e criar um projeto é ação com custo potencial.

### 2. Aplicar as migrações
`0001_esquema.sql` e depois `0002_rls.sql`.

### 3. Exportar as abas da planilha
**Este passo é do usuário — o ambiente do Claude não alcança o Google.**

Na planilha `Buildly3`, para cada aba: *Arquivo → Fazer download → CSV*.
São cinco:

| Aba | Vira a tabela | Colunas |
|---|---|---|
| `Diário` | `rdo` | 25 |
| `Pauta` | `pauta` | 12 |
| `CheckIn` | `checkin` | 12 |
| `Notas Fiscais` | `nota_fiscal` | 10 |
| `Itens NF` | `item_nf` | 7 |

### 4. Converter e importar
`scripts/planilha_para_supabase.py` lê os CSV e gera o SQL de inserção,
conferindo linha a linha. Ele **não inventa dado**: linha que não bate com o
cabeçalho esperado é reportada, não adivinhada.

### 5. Reescrever a camada de dados do app
É a maior parte do trabalho. Hoje o `rdo.html` (7.550 linhas) grava em
`localStorage` e espelha na planilha via Apps Script. Passar para o Supabase
significa trocar essa camada inteira — e é onde mora o risco de perder o que
foi construído nesta semana (chave por apontador, baixa lógica, sincronização
entre aparelhos).

Nenhuma dessas etapas desliga o `buildly2`, que é o que causou o incidente de
26/08. Isso continua sendo ação separada e mais urgente.

---

## O que o cadastro ganha

As tabelas `colaborador`, `atividade`, `equipamento` e `veiculo_leve` **não
existem na planilha**. Hoje o cadastro vive só no `localStorage` de cada
aparelho — por isso cada celular tem a sua lista, e limpar os dados do
navegador apaga tudo. Levá-lo para o banco é o maior ganho isolado desta
migração.

Os campos `inativo` / `inativo_em` / `status_em` reproduzem a regra que o app
já usa: item removido não é apagado, e continua aparecendo nos dias anteriores
à baixa.
