-- LESSON EXAMPLE ONLY. Not shipped to the customer.
-- Recreates the sample customer tables in your own Postgres / Supabase project.
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
