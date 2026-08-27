-- ============================================================
-- BUILDLy — esquema inicial
--
-- Espelha o que hoje vive na planilha do Google (abas Diário, Pauta,
-- CheckIn, Notas Fiscais, Itens NF) e acrescenta o cadastro, que hoje só
-- existe no localStorage de cada aparelho e por isso nunca teve cópia.
--
-- As FOTOS continuam no Google Drive. Aqui guardamos apenas os links, como
-- a planilha já fazia.
--
-- Decisão de forma: nesta primeira etapa as listas do RDO (atividades do
-- dia, efetivo por função, equipamentos usados…) continuam como TEXTO, do
-- jeito que a planilha guarda. Normalizar agora obrigaria a reescrever o
-- app inteiro no mesmo passo da migração de dados — dois riscos de uma vez.
-- Primeiro o dado chega inteiro e conferível; depois se normaliza o que
-- ganhar alguma coisa com isso.
-- ============================================================

create extension if not exists "pgcrypto";

-- ---------- obra ----------
-- O app sempre trabalhou com uma obra por vez, identificada pelo nome — o que
-- criou a armadilha de renomear a obra e "perder" o histórico. Aqui a obra
-- passa a ter identidade própria, e o nome vira só um rótulo editável.
create table obra (
  id          uuid primary key default gen_random_uuid(),
  nome        text not null,
  empresa     text default '',
  cidade      text default '',
  ativa       boolean not null default true,
  criado_em   timestamptz not null default now()
);
create unique index obra_nome_unica on obra (lower(nome));

-- ---------- RDO (aba "Diário") ----------
create table rdo (
  id                        uuid primary key default gen_random_uuid(),
  obra_id                   uuid not null references obra(id) on delete restrict,
  data                      date not null,
  apontador                 text not null,

  dia_semana                text default '',
  local_obra                text default '',
  descricao_local           text default '',
  tempo_clima               text default '',
  jornada                   text default '',
  dss_horario               text default '',
  dss_ministrado_por        text default '',
  dss_tema                  text default '',
  atividades_do_dia         text default '',
  efetivo_total             integer,
  efetivo_por_funcao        text default '',
  colaboradores_presentes   text default '',
  equipamentos_utilizados   text default '',
  veiculos_leves            text default '',
  veiculos_equip_parados    text default '',
  eventos_seguranca         text default '',
  eventos_meio_ambiente     text default '',
  observacoes_do_dia        text default '',
  fotos                     text default '',   -- links do Drive, separados por quebra de linha
  rdo_numero                text default '',

  criado_em                 timestamptz not null default now(),
  atualizado_em             timestamptz not null default now(),
  atualizado_por            text default ''    -- id do aparelho, para resolver conflito
);

-- A regra que o app já aplica: um RDO por apontador por dia. É o que impede
-- o segundo apontador de sobrescrever o diário do primeiro.
create unique index rdo_unico_por_apontador_no_dia
  on rdo (obra_id, data, lower(apontador));
create index rdo_por_data on rdo (obra_id, data desc);

-- ---------- Pauta ----------
create table pauta (
  id               text primary key,
  assunto          text not null,
  descricao        text default '',
  criador          text default '',
  responsavel      text default '',
  setor            text default '',
  prioridade       text not null default 'Média',
  status           text not null default 'Aberta',
  data_lancamento  date,
  data_termino     date,
  criado_em        timestamptz not null default now(),
  atualizado_em    timestamptz not null default now()
);
create index pauta_por_status on pauta (status);

-- ---------- Check-in ----------
create table checkin (
  id               text primary key,
  assunto          text not null,
  descricao        text default '',
  criador          text default '',
  responsavel      text default '',
  setor            text default '',
  prioridade       text not null default 'Média',
  status           text not null default 'Aberta',
  data_termino     date,
  concluido_em     timestamptz,
  criado_em        timestamptz not null default now(),
  atualizado_em    timestamptz not null default now()
);
create index checkin_por_status on checkin (status);

-- ---------- Notas fiscais ----------
create table nota_fiscal (
  id            text primary key,
  numero_nf     text default '',
  serie         text default '',
  data_emissao  date,
  fornecedor    text default '',
  categoria     text default '',
  responsavel   text default '',
  observacoes   text default '',
  total_nf      numeric(14,2),
  foto_url      text default '',   -- foto da nota, no Drive
  criado_em     timestamptz not null default now()
);

create table item_nf (
  id              text primary key,
  nota_fiscal_id  text not null references nota_fiscal(id) on delete cascade,
  numero_nf       text default '',
  descricao       text default '',
  quantidade      numeric(14,3),
  preco_unitario  numeric(14,2),
  total           numeric(14,2)
);
create index item_nf_por_nota on item_nf (nota_fiscal_id);

-- ============================================================
-- CADASTRO
--
-- Isto nunca esteve na planilha: vivia só no localStorage de cada aparelho.
-- Era a razão de o cadastro sumir quando o navegador limpava os dados, e de
-- cada celular ter a sua própria lista.
--
-- Os três campos de baixa vêm da regra que o app já usa: item removido não é
-- apagado, recebe data de baixa, e some apenas dos dias a partir dela — o RDO
-- de ontem continua mostrando quem trabalhou ontem.
-- ============================================================

create table colaborador_categoria (
  id          text primary key,
  obra_id     uuid not null references obra(id) on delete cascade,
  nome        text not null,
  icone       text default '📁',
  inativo     boolean not null default false,
  inativo_em  date,
  status_em   timestamptz not null default now()
);

create table colaborador (
  id            text primary key,
  categoria_id  text not null references colaborador_categoria(id) on delete cascade,
  matricula     text default '',
  nome          text not null,
  funcao        text default '',
  inativo       boolean not null default false,
  inativo_em    date,
  status_em     timestamptz not null default now()
);
create index colaborador_por_categoria on colaborador (categoria_id);

create table atividade (
  id          text primary key,
  obra_id     uuid not null references obra(id) on delete cascade,
  descricao   text not null,
  local       text default '',
  unidade     text default '',
  inativo     boolean not null default false,
  inativo_em  date,
  status_em   timestamptz not null default now()
);

create table equipamento (
  id          text primary key,
  obra_id     uuid not null references obra(id) on delete cascade,
  numero      text default '',
  descricao   text not null,
  inativo     boolean not null default false,
  inativo_em  date,
  status_em   timestamptz not null default now()
);

create table veiculo_leve (
  id          text primary key,
  obra_id     uuid not null references obra(id) on delete cascade,
  descricao   text not null,
  placa       text default '',
  inativo     boolean not null default false,
  inativo_em  date,
  status_em   timestamptz not null default now()
);

-- ---------- atualizado_em automático ----------
-- Sem isto o carimbo dependeria de o app lembrar de mandá-lo, e é justamente
-- ele que decide quem vence quando dois aparelhos editam o mesmo registro.
create or replace function carimbar_atualizacao()
returns trigger language plpgsql as $$
begin
  new.atualizado_em = now();
  return new;
end $$;

create trigger rdo_carimbo     before update on rdo     for each row execute function carimbar_atualizacao();
create trigger pauta_carimbo   before update on pauta   for each row execute function carimbar_atualizacao();
create trigger checkin_carimbo before update on checkin for each row execute function carimbar_atualizacao();
