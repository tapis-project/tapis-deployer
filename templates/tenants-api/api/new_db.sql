DROP database IF EXISTS tenants;

do $$
begin
  create user tenants password 'd3fd6pAssw0rd';
exception
  when others then
    raise notice 'not creating role my_role -- it already exists';
end
$$;

create database tenants owner=tenants;
