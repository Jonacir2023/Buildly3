-- Perfil único (decisão do usuário): qualquer usuário autenticado lê/escreve
-- tudo. Sem autenticação, acesso nenhum. Refinar por papel/obra depois, se
-- o produto evoluir para perfis granulares.
--
-- Nota: o linter do Supabase aponta essas policies como "always true" (WARN).
-- É esperado nesta fase — o controle de acesso hoje é só "autenticado ou não",
-- sem granularidade por obra/papel.

do $$
declare
  r record;
begin
  for r in select tablename from pg_tables where schemaname = 'public' loop
    execute format('alter table public.%I enable row level security', r.tablename);
    execute format(
      'create policy "authenticated_full_access" on public.%I for all to authenticated using (true) with check (true)',
      r.tablename
    );
  end loop;
end $$;
