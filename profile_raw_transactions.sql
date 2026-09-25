-- Read-only profile of tmp_raw_transactions. Returns aggregate counts only, never rows.
-- Query 1: one row per check.  Query 2: row count per expected account.

with t as (select * from tmp_raw_transactions),
expected(account_name) as (values
    ('Chase Checking'), ('Chase Savings'), ('Amex Credit Card'), ('Discover Credit Card')),
exact_dupes as (
    select count(*) as n from t
    group by account_name, txn_date, merchant, amount, category having count(*) > 1),
near_dupes as (
    select count(*) as n, count(distinct merchant) as spellings from t
    group by account_name, txn_date, lower(trim(merchant)), amount having count(*) > 1),
merchant_cats as (
    select lower(trim(merchant)) as m, count(distinct lower(trim(category))) as cats
    from t where category is not null and trim(category) <> '' group by 1),
amount_stats as (
    select avg(abs(amount)) as mean, stddev(abs(amount)) as sd from t)
select 'total rows' as check_name, count(*)::text as value from t
union all select 'date range', min(txn_date) || ' to ' || max(txn_date) from t
union all select 'null account_name', count(*)::text from t where account_name is null
union all select 'null txn_date', count(*)::text from t where txn_date is null
union all select 'null merchant', count(*)::text from t where merchant is null
union all select 'null amount', count(*)::text from t where amount is null
union all select 'null category', count(*)::text from t where category is null
union all select 'blank category', count(*)::text from t where category is not null and trim(category) = ''
union all select 'blank merchant', count(*)::text from t where trim(merchant) = ''
union all select 'exact duplicate groups', count(*)::text from exact_dupes
union all select 'exact duplicate extra rows', coalesce(sum(n - 1), 0)::text from exact_dupes
union all select 'near-duplicate groups (merchant differs only by case/space)', count(*)::text from near_dupes where spellings > 1
union all select 'zero amounts', count(*)::text from t where amount = 0
union all select 'positive amounts', count(*)::text from t where amount > 0
union all select 'negative amounts', count(*)::text from t where amount < 0
union all select 'amount > 3 sd from mean (abs)', count(*)::text from t, amount_stats where abs(amount) > mean + 3 * sd
union all select 'amount with > 2 decimals', count(*)::text from t where amount <> round(amount, 2)
union all select 'future dates (after today)', count(*)::text from t where txn_date > current_date
union all select 'dates before 2000', count(*)::text from t where txn_date < '2000-01-01'
union all select 'merchant with leading/trailing space', count(*)::text from t where merchant <> trim(merchant)
union all select 'merchants with >1 casing/spelling', count(*)::text from (
    select lower(trim(merchant)) from t group by 1 having count(distinct merchant) > 1) x
union all select 'merchants with >1 category', count(*)::text from merchant_cats where cats > 1
union all select 'distinct categories', count(distinct category)::text from t
union all select 'categories differing only by case/space', count(*)::text from (
    select lower(trim(category)) from t where category is not null group by 1 having count(distinct category) > 1) x
union all select 'distinct account names', count(distinct account_name)::text from t
union all select 'rows with unexpected account name', count(*)::text from t where account_name not in (select account_name from expected)
union all select 'expected accounts missing', count(*)::text from expected e where not exists (select 1 from t where t.account_name = e.account_name);

-- Query 2: per-account presence (account names are config, not customer records).
with expected(account_name) as (values
    ('Chase Checking'), ('Chase Savings'), ('Amex Credit Card'), ('Discover Credit Card'))
select coalesce(e.account_name, t.account_name) as account_name,
       e.account_name is not null as expected,
       count(t.id) as rows,
       count(t.id) filter (where t.amount < 0) as negative,
       count(t.id) filter (where t.category is null) as null_category
from expected e
full join tmp_raw_transactions t on t.account_name = e.account_name
group by 1, 2
order by 2 desc, 1;
