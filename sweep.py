from pathlib import Path
from dotenv import load_dotenv
import os
import psycopg

load_dotenv()
url = os.environ["DATABASE_URL"]
system_prompt = Path("system_prompt.md").read_text(encoding="utf-8")

lines = []

with psycopg.connect(url) as conn:
    total_rows = conn.execute("select count(*) from tmp_raw_transactions").fetchone()
    lines.append(f"Total rows: {total_rows[0]}")

    null_categories = conn.execute("select count(*) from tmp_raw_transactions where category is null;").fetchone()
    lines.append(f"Null Categories: {null_categories[0]}")

    missing_accounts = conn.execute("select account_name from (values ('Chase Checking'), ('Chase Savings'), ('Amex Credit Card'), ('Discover Credit Card')) as expected(account_name) except select account_name from tmp_raw_transactions;").fetchall()
    names = ", ".join(row[0] for row in missing_accounts)
    lines.append(f"Missing accounts: {names}")

    duplicates = conn.execute("select account_name, txn_date, lower(trim(merchant)) as merchant, amount, count(*) from tmp_raw_transactions group by account_name, txn_date, lower(trim(merchant)), amount having count(*) > 1;").fetchall()
    lines.append("Duplicate candidates:")
    for account, date, merchant, amount, copies in duplicates:
        lines.append(f"{account} | {date} | {merchant} | {amount} | {copies} copies")

report_input = "\n".join(lines)
print(report_input)