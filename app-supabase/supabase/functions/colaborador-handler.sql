-- Buildly — Funções e Triggers para validações server-side da tabela colaborador
-- Criado: 2026-07-19

-- ============================================================================
-- FUNÇÃO: Validar matrícula única antes de INSERT/UPDATE
-- ============================================================================

create or replace function validar_matricula_unica()
returns trigger as $$
begin
  -- Se matrícula foi fornecida, verificar se é única
  if new.matricula is not null then
    if exists (
      select 1 from colaborador
      where matricula = new.matricula
      and id != new.id
    ) then
      raise exception 'Matrícula % já existe', new.matricula;
    end if;
  end if;
  return new;
end;
$$ language plpgsql;

-- ============================================================================
-- FUNÇÃO: Validar integridade de datas
-- ============================================================================

create or replace function validar_datas_colaborador()
returns trigger as $$
begin
  -- Demissão não pode ser anterior à admissão
  if new.data_demissao is not null and new.data_admissao is not null then
    if new.data_demissao < new.data_admissao then
      raise exception 'Data de demissão não pode ser anterior à admissão';
    end if;
  end if;

  -- Término de experiências devem estar entre admissão e demissão
  if new.data_termino_exp1 is not null and new.data_admissao is not null then
    if new.data_termino_exp1 < new.data_admissao then
      raise exception 'Término 1ª experiência não pode ser anterior à admissão';
    end if;
  end if;

  if new.data_termino_exp2 is not null and new.data_admissao is not null then
    if new.data_termino_exp2 < new.data_admissao then
      raise exception 'Término 2ª experiência não pode ser anterior à admissão';
    end if;
  end if;

  -- Atualizar timestamp de modificação
  new.atualizado_em = now();

  return new;
end;
$$ language plpgsql;

-- ============================================================================
-- FUNÇÃO: Garantir que nome nunca é vazio
-- ============================================================================

create or replace function validar_nome_colaborador()
returns trigger as $$
begin
  if trim(new.nome) = '' then
    raise exception 'Nome do colaborador é obrigatório';
  end if;
  return new;
end;
$$ language plpgsql;

-- ============================================================================
-- TRIGGERS
-- ============================================================================

-- Validar matrícula ao INSERT ou UPDATE
drop trigger if exists tr_validar_matricula on colaborador;
create trigger tr_validar_matricula
  before insert or update on colaborador
  for each row
  execute function validar_matricula_unica();

-- Validar datas ao INSERT ou UPDATE
drop trigger if exists tr_validar_datas on colaborador;
create trigger tr_validar_datas
  before insert or update on colaborador
  for each row
  execute function validar_datas_colaborador();

-- Validar nome ao INSERT ou UPDATE
drop trigger if exists tr_validar_nome on colaborador;
create trigger tr_validar_nome
  before insert or update on colaborador
  for each row
  execute function validar_nome_colaborador();

-- ============================================================================
-- VIEWS ÚTEIS PARA CONSULTAS
-- ============================================================================

-- View: Colaboradores ativos por frente
create or replace view v_colaboradores_ativos_por_frente as
select
  frente_servico,
  count(*) as total_colaboradores,
  count(case when situacao = 'ativo' then 1 end) as ativos,
  count(case when situacao = 'inativo' then 1 end) as inativos,
  count(case when situacao = 'afastado' then 1 end) as afastados
from colaborador
where frente_servico is not null
group by frente_servico
order by frente_servico;

-- View: Collaboradores com supervisor (hierarquia)
create or replace view v_hierarquia_colaboradores as
select
  c.id,
  c.nome,
  c.cargo,
  c.frente_servico,
  s.nome as supervisor_nome,
  s.cargo as supervisor_cargo
from colaborador c
left join colaborador s on c.supervisor_id = s.id
order by c.frente_servico, s.nome, c.nome;

-- View: Contratos de experiência vencendo
create or replace view v_experimentos_vencendo as
select
  id,
  nome,
  cargo,
  data_termino_exp1,
  data_termino_exp2,
  (data_termino_exp1 - current_date) as dias_para_vencer_exp1,
  (data_termino_exp2 - current_date) as dias_para_vencer_exp2
from colaborador
where
  (data_termino_exp1 is not null and data_termino_exp1 <= current_date + interval '30 days')
  or (data_termino_exp2 is not null and data_termino_exp2 <= current_date + interval '30 days')
order by data_termino_exp1, data_termino_exp2;

