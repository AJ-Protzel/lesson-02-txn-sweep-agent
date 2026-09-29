from pathlib import Path
from claude_backend import call_cli
from config import CATEGORIES

category_lines = "\n".join(f"{name}: {desc}" for name, desc in CATEGORIES.items())
categorize_prompt = Path("categorize_prompt.md").read_text(encoding="utf-8").format(categories=category_lines)

# Temporary until .env exists; replaced by a select distinct merchant query.
merchants = ["Amazon", "Chevron", "Netflix", "PG&E", "Safeway",
             "Shell Gas", "Spotify", "Starbucks", "Target", "Trader Joe's"]

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
    for merchant, category in categorize(merchants).items():
        print(f"{merchant}: {category}")