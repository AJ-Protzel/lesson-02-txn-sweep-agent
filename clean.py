import os
import psycopg
from pathlib import Path
from dotenv import load_dotenv
from claude_backend import call_cli
from config import CATEGORIES

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

if __name__ == "__main__":
    for merchant, category in categorize(get_merchants()).items():
        print(f"{merchant}: {category}")