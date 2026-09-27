from pathlib import Path
from dotenv import load_dotenv
import os
import psycopg

load_dotenv()
url = os.environ["DATABASE_URL"]
system_prompt = Path("system_prompt.md").read_text(encoding="utf-8")

with psycopg.connect(url) as conn:
    row = conn.execute("select count(*) from tmp_raw_transactions").fetchone()
    print(row)