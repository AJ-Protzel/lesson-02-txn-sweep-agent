import os
import psycopg
from pathlib import Path
from dotenv import load_dotenv
from claude_backend import call_cli
from config import EXPECTED_ACCOUNTS

load_dotenv()
url = os.environ["DATABASE_URL"]
system_prompt = Path("system_prompt.md").read_text(encoding="utf-8")

def run_sweep(runs = 2):
    replies = []
    lines = []

    with psycopg.connect(url) as conn:
        total_rows = conn.execute("select count(*) from tmp_raw_transactions").fetchone()
        lines.append(f"Total rows: {total_rows[0]}")

        null_categories = conn.execute("select count(*) from tmp_raw_transactions where category is null;").fetchone()
        lines.append(f"Null Categories: {null_categories[0]}")

        missing_accounts = conn.execute(
            """
            SELECT account_name
            FROM unnest(%s::text[]) AS expected(account_name)
            EXCEPT
            SELECT account_name
            FROM tmp_raw_transactions
            """,
            [EXPECTED_ACCOUNTS],
        ).fetchall()

        names = ", ".join(row[0] for row in missing_accounts)
        lines.append(f"Missing accounts: {len(missing_accounts)} — {names or 'none'}")

        duplicates = conn.execute("select account_name, txn_date, lower(trim(merchant)) as merchant, amount, count(*) from tmp_raw_transactions group by account_name, txn_date, lower(trim(merchant)), amount having count(*) > 1 order by txn_date;").fetchall()
        lines.append("Duplicate candidates:\naccount | date | merchant | amount | amount_size | copies")
        for account, date, merchant, amount, copies in duplicates:
            if amount > 60:
                amount_size = "Large"
            else:
                amount_size = "Small"

            lines.append(f"{account} | {date} | {merchant} | {amount} | {amount_size} | {copies} copies on this date")

    report_input = "\n".join(lines)

    for run in range(runs):
        reply = call_cli([{"role": "user", "content": report_input}], system=system_prompt)
        replies.append(reply)

    return replies

if __name__ == "__main__":
    for number, reply in enumerate(run_sweep(), start=1):
        print(f"--- run {number} ---")
        print(reply)