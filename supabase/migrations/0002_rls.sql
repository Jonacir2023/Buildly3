-- ============================================================
-- BUILDLy — quem pode ler e escrever
--
-- Isto não é detalhe de configuração: é a diferença entre um banco privado e
-- um banco público. O app é uma página estática, e numa página estática a
-- chave anon É PÚBLICA — qualquer pessoa que abrir o código-fonte a enxerga.
-- A única coisa que separa o dado da internet inteira são as políticas abaixo.
--
-- Regra desta etapa: nada é legível sem login. Quem está autenticado enxerga
-- e edita tudo — é o time da obra inteiro, e ainda não há motivo para separar
-- por pessoa. Quando houver (por exemplo, apontador só edita o próprio RDO),
-- a política vira uma comparação com auth.uid() e nada mais precisa mudar.
-- ============================================================

alter table obra                  enable row level security;
alter table rdo                   enable row level security;
alter table pauta                 enable row level security;
alter table checkin               enable row level security;
alter table nota_fiscal           enable row level security;
alter table item_nf               enable row level security;
alter table colaborador_categoria enable row level security;
alter table colaborador           enable row level security;
alter table atividade             enable row level security;
alter table equipamento           enable row level security;
alter table veiculo_leve          enable row level security;

do $$
declare t text;
begin
  foreach t in array array[
    'obra','rdo','pauta','checkin','nota_fiscal','item_nf',
    'colaborador_categoria','colaborador','atividade','equipamento','veiculo_leve'
  ] loop
    execute format(
      'create policy %I on %I for all to authenticated using (true) with check (true)',
      t || '_autenticado', t);
  end loop;
end $$;

-- Cinto e suspensório: além de não ter política, o papel anon perde o próprio
-- acesso às tabelas. O Supabase concede esse acesso por padrão a tudo que
-- nasce no schema public, e é só a política que segura. Revogando aqui, uma
-- política permissiva criada por engano no futuro ainda não abriria o banco.
revoke all on all tables in schema public from anon;
alter default privileges in schema public revoke all on tables from anon;

-- Nenhuma política para o papel anon: sem login, o banco responde vazio.
-- É proposital. Se algum dia uma tela precisar ser pública, a política entra
-- aqui explicitamente, tabela por tabela — nunca por falta de política.
