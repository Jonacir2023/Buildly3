-- Buildly — Expansão da tabela colaborador com 20 campos operacionais de canteiro
-- Adicionados: 2026-07-19
-- Escopo: Dados operacionais para planejamento, relatórios e operações diárias
-- NÃO incluem dados de RH/eSocial (compliance)

-- ============================================================================
-- ENUM TYPES — 6 tipos para campos com valores fixos
-- ============================================================================

-- Situação do colaborador: ativo, inativo, afastado ou em licença
create type situacao_enum as enum (
  'ativo',
  'inativo',
  'afastado',
  'licença'
);

-- Tipo de mão de obra: direta (mod), indireta (moi) ou terceirizada
create type tipo_mao_obra_enum as enum (
  'moi',           -- Mão de obra indireta
  'mod',           -- Mão de obra direta
  'terceirizado'
);

-- Sexo do colaborador
create type sexo_enum as enum (
  'masculino',
  'feminino',
  'não_informado'
);

-- Estado/UF — 27 opciones (26 estados + DF)
create type estado_enum as enum (
  'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
  'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
  'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
);

-- Status da mobilização: processo de integração/contratação
create type status_mobilizacao_enum as enum (
  'não_iniciado',
  'em_progresso',
  'concluído',
  'cancelado'
);

-- Status de alojamento: necessidade de hospedagem
create type status_alojamento_enum as enum (
  'não_necessário',
  'necessário',
  'fornecido',
  'recusado'
);

-- ============================================================================
-- ALTERAÇÕES NA TABELA COLABORADOR
-- ============================================================================

alter table colaborador add column (
  -- Identificação e Dados Pessoais (7 campos)
  matricula integer unique,                              -- Matrícula única
  data_admissao date,                                    -- Data de admissão
  data_demissao date,                                    -- Data de demissão (nullable)
  situacao situacao_enum default 'ativo',               -- Situação atual
  cargo text,                                            -- Cargo operacional
  tipo_mao_obra tipo_mao_obra_enum,                     -- Tipo de mão de obra
  estabilidade text,                                     -- Status de estabilidade

  -- Localização (4 campos)
  cidade text,                                           -- Cidade de trabalho
  estado estado_enum,                                    -- Estado/UF

  -- Dados Pessoais Complementares (1 campo)
  sexo sexo_enum default 'não_informado',               -- Sexo

  -- Registro e Mobil​ização (3 campos)
  local_registro text,                                   -- Local de registro
  status_mobilizacao status_mobilizacao_enum default 'não_iniciado', -- Status mobilização
  status_alojamento status_alojamento_enum default 'não_necessário',  -- Status alojamento

  -- Contratos de Experiência (2 campos)
  data_termino_exp1 date,                                -- Término 1ª experiência
  data_termino_exp2 date,                                -- Término 2ª experiência

  -- Relacionamentos (2 campos)
  eng_responsavel_id uuid,                               -- FK: Engenheiro responsável
  supervisor_id uuid,                                    -- FK: Supervisor (self-ref)

  -- Operacional (1 campo)
  frente_servico text,                                   -- Frente/seção de trabalho

  -- Auditoria (1 campo)
  atualizado_em timestamptz default now()               -- Última atualização
);

-- ============================================================================
-- FOREIGN KEY CONSTRAINTS
-- ============================================================================

-- Supervisor é uma auto-referência a outro colaborador
alter table colaborador
  add constraint fk_supervisor
  foreign key (supervisor_id)
  references colaborador(id) on delete set null;

-- eng_responsavel_id referencia tabela de usuários/engenheiros (se existir)
-- Descomentar quando tabela de usuários for criada:
-- alter table colaborador
--   add constraint fk_eng_responsavel
--   foreign key (eng_responsavel_id)
--   references usuarios(id) on delete set null;

-- ============================================================================
-- ÍNDICES PARA PERFORMANCE
-- ============================================================================

-- Buscas por empresa (já existe em queries)
create index idx_colaborador_empresa on colaborador(empresa);

-- Buscas por situação (filtros comuns)
create index idx_colaborador_situacao on colaborador(situacao);

-- Buscas por frente de serviço (alocação de recursos)
create index idx_colaborador_frente_servico on colaborador(frente_servico);

-- Hierarquia de supervisão
create index idx_colaborador_supervisor on colaborador(supervisor_id);

-- Buscas por matrícula
create index idx_colaborador_matricula on colaborador(matricula);

-- Buscas por status de mobilização
create index idx_colaborador_mobilizacao on colaborador(status_mobilizacao);

-- ============================================================================
-- COMENTÁRIOS DE DOCUMENTAÇÃO
-- ============================================================================

comment on table colaborador is 'Cadastro de colaboradores com dados operacionais de canteiro (não inclui dados de RH/eSocial)';

comment on column colaborador.matricula is 'Número único de matrícula do colaborador';
comment on column colaborador.data_admissao is 'Data de admissão na obra';
comment on column colaborador.data_demissao is 'Data de demissão (null se ainda ativo)';
comment on column colaborador.situacao is 'Situação atual: ativo, inativo, afastado, licença';
comment on column colaborador.cargo is 'Cargo operacional (ex: pedreiro, encarregado, etc.)';
comment on column colaborador.tipo_mao_obra is 'Tipo de mão de obra: MOI, MOD ou terceirizado';
comment on column colaborador.estabilidade is 'Status de estabilidade (ex: até 30/06/2026)';
comment on column colaborador.cidade is 'Cidade de trabalho';
comment on column colaborador.estado is 'Estado/UF de trabalho';
comment on column colaborador.sexo is 'Sexo do colaborador';
comment on column colaborador.local_registro is 'Local de registro para RH';
comment on column colaborador.status_mobilizacao is 'Status do processo de mobilização';
comment on column colaborador.status_alojamento is 'Necessidade e status de alojamento';
comment on column colaborador.data_termino_exp1 is 'Data de término do contrato de experiência 1';
comment on column colaborador.data_termino_exp2 is 'Data de término do contrato de experiência 2';
comment on column colaborador.eng_responsavel_id is 'Referência ao engenheiro responsável';
comment on column colaborador.supervisor_id is 'Referência ao encarregado/supervisor';
comment on column colaborador.frente_servico is 'Frente/seção de trabalho';
comment on column colaborador.atualizado_em is 'Timestamp da última atualização';

