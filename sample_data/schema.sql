-- LESSON EXAMPLE ONLY. Not shipped to the customer.
-- Recreates the sample customer tables and roles in your own Postgres / Supabase project.
-- Snapshot taken 2026-09-22; the data is generated, not real.

create table if not exists tmp_raw_transactions (
    id           serial primary key,
    account_name text    not null,
    txn_date     date    not null,
    merchant     text    not null,
    amount       numeric not null,
    category     text
);

-- Built by clean.py in phase 2; empty in the snapshot.
create table if not exists tmp_category_map (
    merchant text primary key,
    category text not null
);

create table if not exists tmp_clean_transactions (
    id           integer primary key,
    account_name text    not null,
    txn_date     date    not null,
    merchant     text    not null,
    amount       numeric not null,
    category     text    not null
);

-- Load the rows (psql, from the repo root):
--   \copy tmp_raw_transactions from 'sample_data/raw_transactions.csv' with (format csv, header true)
--   select setval('tmp_raw_transactions_id_seq', (select max(id) from tmp_raw_transactions));
-- In the Supabase dashboard, use Table Editor > Import data from CSV instead.

-- Least-access roles, one per phase. Pick your own passwords.
-- sweep_reader (phase 1, DATABASE_URL): read the raw table only.
-- sweep_writer (phase 2, CLEAN_DATABASE_URL): read raw, write the two tables it builds.
create role sweep_reader login password '<choose one>';
create role sweep_writer login password '<choose one>';

grant select on tmp_raw_transactions to sweep_reader, sweep_writer;
grant select, insert, update, delete on tmp_category_map, tmp_clean_transactions to sweep_writer;

-- With row level security on (Supabase default), each role also needs a policy.
alter table tmp_raw_transactions enable row level security;
alter table tmp_category_map enable row level security;
alter table tmp_clean_transactions enable row level security;
create policy sweep_reader_select on tmp_raw_transactions for select to sweep_reader using (true);
create policy sweep_writer_select on tmp_raw_transactions for select to sweep_writer using (true);
create policy sweep_writer_all on tmp_category_map for all to sweep_writer using (true) with check (true);
create policy sweep_writer_all on tmp_clean_transactions for all to sweep_writer using (true) with check (true);
