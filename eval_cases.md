# Eval cases

## Phase 1

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



## Phase 2

Expected answers computed by hand from tmp_raw_transactions (103 rows) on 2026-09-29.

## 4. Merchant map
Expected: 10 merchants, each with exactly one expected category.
How I got it:
```sql
select distinct merchant
from tmp_raw_transactions
order by 1;
```
Why: Transactions were miscategorized.
Which ones:
- Amazon: Shopping
- Chevron: Gas
- Netflix: Subscriptions
- PG&E: Bills
- Safeway: Groceries
- Shell Gas: Gas
- Spotify: Subscriptions
- Starbucks: Dining
- Target: Shopping
- Trader Joe's: Groceries

## 5. Null categories
Expected: 0
How I got it:
by rule.
Why: Every transaction should have a mapped category.
Which ones:
- The 23 raw rows with null categories.

## 6. Allowed categories
Expected: 0 categories outside config.CATEGORIES.
How I got it:
by rule.
Why: A category count can be correct while the category names are wrong.
Which ones:
- Every category in the clean table.

## 7. Rows match the map
Expected: 0 category mismatches.
How I got it:
by rule.
Why: The mapped category should replace the raw category.
Which ones:
- All retained transactions, including those with null or incorrect raw categories.

## 8. Duplicates dropped
Expected: 102 clean rows (103 raw rows minus 1 confirmed extra row).
How I got it:
```sql
select count(*)
from tmp_raw_transactions;
```
```sql
select id, account_name, txn_date, merchant, amount, category
from (
    select *,
           count(*) over (
               partition by account_name, txn_date, lower(trim(merchant)), amount
           ) as copies
    from tmp_raw_transactions
) as candidates
where copies > 1
order by account_name, txn_date, lower(trim(merchant)), amount, id;
```
Why: Only Safeway is confirmed for removal so far. Netflix and Spotify stay until the customer answers.
Which ones:
| id | account_name | txn_date | merchant | amount | category |
|---|---|---|---|---|---|
| 14 | Amex Credit Card | 2026-09-08 | Netflix | 15.49 | Subscriptions |
| 60 | Amex Credit Card | 2026-09-08 | Netflix | 15.49 | Subscriptions |
| 33 | Amex Credit Card | 2026-09-10 | Netflix | 15.49 | Subscriptions |
| 42 | Amex Credit Card | 2026-09-10 | Netflix | 15.49 | Subscriptions |
| 21 | Chase Checking | 2026-09-14 | Safeway | 84.23 | Groceries |
| 95 | Chase Checking | 2026-09-14 | Safeway | 84.23 | Groceries |
| 61 | Chase Savings | 2026-09-21 | Spotify | 11.99 | Shopping |
| 81 | Chase Savings | 2026-09-21 | Spotify | 11.99 | Utilities |
Safeway: keep 21, drop 95. Netflix (14, 60, 33, 42) and Spotify (61, 81): keep all until the customer answers.

## 9. Nothing else changed
Expected: 0 changes to retained rows' id, account_name, txn_date, merchant, or amount.
How I got it:
by rule.
Why: Category mapping and duplicate removal should not change other transaction details.
Which ones:
- All 102 retained rows.

## 10. Accounts
Expected: The clean table has the same accounts as the raw table. Discover Credit Card is still missing.
How I got it:
```sql
select distinct account_name
from tmp_raw_transactions
order by 1;
```
Why: Cleaning cannot create missing account transactions. Discover remains a customer-side fix.
Which ones:
- Chase Checking: present.
- Chase Savings: present.
- Amex Credit Card: present.
- Discover Credit Card: missing.



## Cases to test later
- Real repeats (two coffees the same day)
- Pending then posted
- Uber Eats vs Uber categorization
