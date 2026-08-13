-- Buildly — schema inicial
-- Baseado na especificação inicial (módulos MVP): obras, RDO, efetivo, GED,
-- segurança do trabalho, estoque, tarefas/atas, planejamento, orçamento,
-- fornecedores/terceiros.

create extension if not exists "pgcrypto";

-- ---------------------------------------------------------------------------
-- Obra
-- ---------------------------------------------------------------------------

create table obra (
  id uuid primary key default gen_random_uuid(),
  nome text not null,
  endereco text,
  cliente text,
  construtora text,
  latitude double precision,
  longitude double precision,
  area_m2 numeric,
  tipologia text,
  data_inicio date,
  data_termino_prevista date,
  criado_em timestamptz not null default now()
);

-- ---------------------------------------------------------------------------
-- Colaborador / Efetivo
-- ---------------------------------------------------------------------------

create table colaborador (
  id uuid primary key default gen_random_uuid(),
  nome text not null,
  empresa text,
  funcao text,
  criado_em timestamptz not null default now()
);

create table efetivo_registro (
  id uuid primary key default gen_random_uuid(),
  obra_id uuid not null references obra(id) on delete cascade,
  colaborador_id uuid not null references colaborador(id),
  data date not null,
  presente boolean not null default true,
  criado_em timestamptz not null default now(),
  unique (obra_id, colaborador_id, data)
);

-- ---------------------------------------------------------------------------
-- RDO (Diário de Obras)
-- ---------------------------------------------------------------------------

create type rdo_status as enum ('rascunho', 'em_aprovacao', 'aprovado', 'rejeitado');
create type rdo_periodo as enum ('madrugada', 'manha', 'tarde', 'noite');
create type rdo_condicao_area as enum ('operavel', 'inoperavel', 'parcialmente_operavel');

create table rdo (
  id uuid primary key default gen_random_uuid(),
  obra_id uuid not null references obra(id) on delete cascade,
  data date not null,
  responsavel_id uuid references colaborador(id),
  status rdo_status not null default 'rascunho',
  edicao_bloqueada boolean not null default false,
  condicao_area rdo_condicao_area,
  observacoes_condicoes text,
  criado_em timestamptz not null default now(),
  atualizado_em timestamptz not null default now(),
  unique (obra_id, data)
);

create table rdo_clima (
  id uuid primary key default gen_random_uuid(),
  rdo_id uuid not null references rdo(id) on delete cascade,
  periodo rdo_periodo not null,
  condicao text,
  precipitacao_mm numeric default 0,
  ativo boolean not null default false,
  origem text default 'manual', -- 'manual' | 'open-meteo'
  unique (rdo_id, periodo)
);

create table rdo_atividade (
  id uuid primary key default gen_random_uuid(),
  rdo_id uuid not null references rdo(id) on delete cascade,
  descricao text not null,
  percentual_executado numeric,
  responsavel text
);

create table rdo_maquina (
  id uuid primary key default gen_random_uuid(),
  rdo_id uuid not null references rdo(id) on delete cascade,
  equipamento text not null,
  quantidade integer default 1,
  horas_operacao numeric,
  situacao text
);

create table rdo_ocorrencia (
  id uuid primary key default gen_random_uuid(),
  rdo_id uuid not null references rdo(id) on delete cascade,
  tipo text,
  descricao text not null,
  gravidade text
);

create table rdo_anexo (
  id uuid primary key default gen_random_uuid(),
  rdo_id uuid not null references rdo(id) on delete cascade,
  rdo_atividade_id uuid references rdo_atividade(id),
  arquivo_url text not null,
  tipo text,
  criado_em timestamptz not null default now()
);

create table rdo_parecer_juridico (
  rdo_id uuid primary key references rdo(id) on delete cascade,
  texto text,
  autor_id uuid references colaborador(id),
  atualizado_em timestamptz not null default now()
);

-- ---------------------------------------------------------------------------
-- GED
-- ---------------------------------------------------------------------------

create table documento (
  id uuid primary key default gen_random_uuid(),
  obra_id uuid not null references obra(id) on delete cascade,
  categoria text,
  nome text not null,
  arquivo_url text not null,
  versao integer default 1,
  enviado_por uuid references colaborador(id),
  criado_em timestamptz not null default now()
);

-- ---------------------------------------------------------------------------
-- Segurança do Trabalho
-- ---------------------------------------------------------------------------

create table sst_registro (
  id uuid primary key default gen_random_uuid(),
  obra_id uuid not null references obra(id) on delete cascade,
  data date not null,
  tipo text not null, -- 'dds' | 'ocorrencia' | 'checklist_epi'
  descricao text,
  responsavel_id uuid references colaborador(id),
  criado_em timestamptz not null default now()
);

-- ---------------------------------------------------------------------------
-- Controle de Estoque
-- ---------------------------------------------------------------------------

create type estoque_nf_status as enum ('upload', 'revisao', 'confirmado', 'avaliado');

create table estoque_nf (
  id uuid primary key default gen_random_uuid(),
  obra_id uuid not null references obra(id) on delete cascade,
  arquivo_foto_url text,
  status estoque_nf_status not null default 'upload',
  fornecedor_cnpj text,
  valor_total numeric,
  extraido_por_ia boolean default false,
  criado_em timestamptz not null default now()
);

create table estoque_item (
  id uuid primary key default gen_random_uuid(),
  nf_id uuid not null references estoque_nf(id) on delete cascade,
  descricao text not null,
  quantidade numeric not null,
  unidade text,
  valor_unitario numeric,
  origem text default 'manual' -- 'ia' | 'manual'
);

create table estoque_saldo (
  id uuid primary key default gen_random_uuid(),
  obra_id uuid not null references obra(id) on delete cascade,
  item_descricao text not null,
  quantidade_atual numeric not null default 0,
  valor_estoque numeric default 0,
  unique (obra_id, item_descricao)
);

create table estoque_perda (
  id uuid primary key default gen_random_uuid(),
  obra_id uuid not null references obra(id) on delete cascade,
  item_descricao text not null,
  quantidade numeric not null,
  motivo text,
  data date not null default current_date
);

-- ---------------------------------------------------------------------------
-- Contrato / Cronograma (base para conferência das atas)
-- ---------------------------------------------------------------------------

create table contrato (
  id uuid primary key default gen_random_uuid(),
  obra_id uuid not null references obra(id) on delete cascade,
  numero text,
  contratante text,
  contratada text,
  arquivo_url text,
  criado_em timestamptz not null default now()
);

create table contrato_clausula (
  id uuid primary key default gen_random_uuid(),
  contrato_id uuid not null references contrato(id) on delete cascade,
  identificador text, -- ex: "Cláusula 4.2"
  texto text not null
);

create table cronograma (
  id uuid primary key default gen_random_uuid(),
  obra_id uuid not null references obra(id) on delete cascade,
  origem text default 'manual', -- 'importado' | 'manual'
  criado_em timestamptz not null default now()
);

create table cronograma_marco (
  id uuid primary key default gen_random_uuid(),
  cronograma_id uuid not null references cronograma(id) on delete cascade,
  nome text not null,
  data_prevista date,
  data_realizada date,
  percentual_previsto numeric,
  percentual_realizado numeric
);

-- ---------------------------------------------------------------------------
-- Tarefas / Ata de Reunião
-- (reaproveita o conceito Tarefa/Checkin/Pauta já usado no vault JC)
-- ---------------------------------------------------------------------------

create table tarefa (
  id uuid primary key default gen_random_uuid(),
  obra_id uuid not null references obra(id) on delete cascade,
  assunto text not null,
  descricao text,
  criador text,
  responsavel text,
  setor text,
  prioridade text,
  status text not null default 'Aberta',
  data_lancamento date default current_date,
  previsao_termino date,
  criado_em timestamptz not null default now()
);

create table ata_reuniao (
  id uuid primary key default gen_random_uuid(),
  obra_id uuid not null references obra(id) on delete cascade,
  data date not null,
  hora time,
  participantes text,
  criado_em timestamptz not null default now()
);

create table ata_item (
  id uuid primary key default gen_random_uuid(),
  ata_id uuid not null references ata_reuniao(id) on delete cascade,
  assunto text not null,
  descricao text
);

create type ata_referencia_tipo as enum ('contrato', 'cronograma');
create type ata_encontrada_por as enum ('ia', 'humano');

create table ata_discrepancia (
  id uuid primary key default gen_random_uuid(),
  ata_item_id uuid not null references ata_item(id) on delete cascade,
  encontrada_por ata_encontrada_por not null default 'ia',
  referencia_tipo ata_referencia_tipo not null,
  referencia_id uuid, -- aponta para contrato_clausula.id ou cronograma_marco.id
  descricao_divergencia text not null,
  data_analise timestamptz not null default now()
);

-- ---------------------------------------------------------------------------
-- Orçamento
-- ---------------------------------------------------------------------------

create table orcamento_item (
  id uuid primary key default gen_random_uuid(),
  obra_id uuid not null references obra(id) on delete cascade,
  categoria text,
  item text not null,
  valor_previsto numeric,
  valor_realizado numeric default 0
);

-- ---------------------------------------------------------------------------
-- Fornecedores / Terceiros
-- ---------------------------------------------------------------------------

create table terceiro (
  id uuid primary key default gen_random_uuid(),
  obra_id uuid not null references obra(id) on delete cascade,
  razao_social text not null,
  cnpj text
);

create type terceiro_doc_status as enum ('pendente', 'aprovado', 'rejeitado');

create table terceiro_documento (
  id uuid primary key default gen_random_uuid(),
  terceiro_id uuid not null references terceiro(id) on delete cascade,
  tipo text not null, -- 'cartao_cnpj' | 'contrato_social' | 'alvara' | 'cnd' | ...
  arquivo_url text,
  status terceiro_doc_status not null default 'pendente',
  mes_referencia date
);

create table terceiro_contrato (
  id uuid primary key default gen_random_uuid(),
  terceiro_id uuid not null references terceiro(id) on delete cascade,
  status terceiro_doc_status not null default 'pendente',
  arquivo_url text
);
