import os
import psycopg
from pathlib import Path
from dotenv import load_dotenv
from claude_backend import call_cli
from config import CATEGORIES, CONFIRMED_DUPLICATE_IDS

load_dotenv()
url = os.environ["CLEAN_DATABASE_URL"]
category_lines = "\n".join(f"{name}: {desc}" for name, desc in CATEGORIES.items())
categorize_prompt = Path("categorize_prompt.md").read_text(encoding="utf-8").format(categories=category_lines)

def get_merchants():
    with psycopg.connect(url) as conn:
        rows = conn.execute("select distinct merchant from tmp_raw_transactions order by merchant").fetchall()
    return [row[0] for row in rows]

def categorize(merchants):
    reply = call_cli([{"role": "user", "content": "\n".join(merchants)}], system=categorize_prompt)

    category_map = {}
    for line in reply.splitlines():
        if ":" in line:
            merchant, category = line.rsplit(":", 1)
            merchant = merchant.strip()
            if merchant in category_map:
                raise ValueError(f"Claude listed {merchant} twice")
            category_map[merchant] = category.strip()

    return category_map

def write_clean(category_map):
    # One transaction: if any step fails, both tables keep their old contents.
    with psycopg.connect(url) as conn:
        conn.execute("delete from tmp_category_map")
        for merchant, category in category_map.items():
            conn.execute(
                "insert into tmp_category_map (merchant, category) values (%s, %s)",
                [merchant, category],
            )

        conn.execute("delete from tmp_clean_transactions")
        conn.execute(
            """
            insert into tmp_clean_transactions (id, account_name, txn_date, merchant, amount, category)
            select raw.id, raw.account_name, raw.txn_date, raw.merchant, raw.amount, map.category
            from tmp_raw_transactions as raw
            left join tmp_category_map as map on map.merchant = raw.merchant
            where raw.id <> all(%s)
            """,
            [CONFIRMED_DUPLICATE_IDS],
        )

        return conn.execute("select count(*) from tmp_clean_transactions").fetchone()[0]

if __name__ == "__main__":
    category_map = categorize(get_merchants())
    for merchant, category in category_map.items():
        print(f"{merchant}: {category}")
    print(f"Clean rows: {write_clean(category_map)}")