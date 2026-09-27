# Eval cases

Expected answers computed by hand from tmp_raw_transactions (103 rows) on 2026-09-27.

## 1. Null categories
Expected: 23
How I got it:
```sql
select count(*) from tmp_raw_transactions where category is null;
```

## 2. Missing accounts
Expected: Discover Credit Card
How I got it: 
```sql
select account_name
from (values ('Chase Checking'), ('Chase Savings'), ('Amex Credit Card'), ('Discover Credit Card')) as expected(account_name)
except
select account_name from tmp_raw_transactions;
```

## 3. Duplicate charges
Expected: 4 duplicate groups (4 extra rows)
How I got it:
```sql
select account_name, txn_date, lower(trim(merchant)) as merchant, amount, count(*)
from tmp_raw_transactions
group by account_name, txn_date, lower(trim(merchant)), amount
having count(*) > 1;
```
why: category is excluded for being a row description and not something that makes up a transaction.
Which ones:
| account_name | txn_date | merchant | amount | count |
|---|---|---|---|---|
| Chase Checking | 2026-09-14 | safeway | 84.23 | 2 |
| Amex Credit Card | 2026-09-10 | netflix | 15.49 | 2 |
| Amex Credit Card | 2026-09-08 | netflix | 15.49 | 2 |
| Chase Savings | 2026-09-21 | spotify | 11.99 | 2 |

Expected verdict: all four groups are genuine duplicates. For the Safeway group, the matching charges are for a large, specific amount. Because Safeway is a grocery store, that amount likely reflects a full shopping trip. It is unlikely that the customer bought the same cart of groceries twice. Netflix on 9/8 and 9/10 are two separate groups, each a same-day pair; merging them into one pair is a fail.

## Cases to test later
- Real repeats (two coffees the same day)
- Pending then posted
- Wrong account: Spotify subscription charged to Chase Savings