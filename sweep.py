from pathlib import Path
from dotenv import load_dotenv
import os
import psycopg

load_dotenv()
url = os.environ["DATABASE_URL"]
system_prompt = Path("system_prompt.md").read_text(encoding="utf-8")

with psycopg.connect(url) as conn:
    total_rows = conn.execute("select count(*) from tmp_raw_transactions").fetchone()
    print(total_rows[0])

    null_categories = conn.execute("select count(*) from tmp_raw_transactions where category is null;").fetchone()
    print(null_categories[0])

    missing_accounts = conn.execute("select account_name from (values ('Chase Checking'), ('Chase Savings'), ('Amex Credit Card'), ('Discover Credit Card')) as expected(account_name) except select account_name from tmp_raw_transactions;").fetchall()
    print(missing_accounts[0])

    duplicates = conn.execute("select account_name, txn_date, lower(trim(merchant)) as merchant, amount, count(*) from tmp_raw_transactions group by account_name, txn_date, lower(trim(merchant)), amount having count(*) > 1;").fetchall()
    print(duplicates)