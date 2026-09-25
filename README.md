# lesson-02-txn-sweep-agent

An agent that sweeps a customer's Supabase transaction table, reports what is
wrong with it, and later cleans it and sends a weekly wrap-up.

Second in a series of small agent projects; a more hands-on redo of
[lesson-01-csv-qa-agent](https://github.com/AJ-Protzel/lesson-01-csv-qa-agent).

## The customer

The customer aggregates their bank transactions into Supabase through
SimpleFIN. They have no checks or reports, so the table is raw bank data that
has never been cleaned. We host the agent; the customer owns and holds the
Supabase keys and the Claude API keys.

They expect four accounts in their data:

- Chase Checking
- Chase Savings
- Amex Credit Card
- Discover Credit Card

## Plan

| step | what | access | status |
|---|---|---|---|
| 1 | Sweep the table: find data errors, check every expected account is present | read-only key | next |
| 2 | Fix what the sweep found | write key from the customer | not started |
| 3 | Weekly wrap-up email on the database, then hand off the agent | write key | not started |

Step 1 is read-only. Nothing is written to the customer's database until they
hand over a write key.

## Install

```bash
pip install -r requirements.txt
```

## Calling Claude

`claude_backend.py` gives every entry point the same two backends, as in
lesson 1:

| flag | how it calls Claude | needs |
|---|---|---|
| `--backend api` (default) | Anthropic API via the Python SDK | `ANTHROPIC_API_KEY` set; bills API credits |
| `--backend cli` | `claude -p`, Claude Code's scripting mode | Claude Code installed and logged in; uses the subscription |

Defaults are `--model claude-sonnet-5 --effort medium`. The `cli` backend runs
with no tools and strips `ANTHROPIC_API_KEY` from its environment so it never
bills the API by accident.

## Sample data

`sample_data/` is a snapshot of the customer's tables so anyone who clones the
repo can run the agent without access to the live database. It is generated
data, not real transactions.

| file | contents |
|---|---|
| `raw_transactions.csv` | 103 rows, 2026-09-02 to 2026-09-21, taken 2026-09-22 |
| `schema.sql` | creates `tmp_raw_transactions` and `tmp_clean_transactions` and shows how to load the CSV |

The clean table was empty at snapshot time. Discover Credit Card is
deliberately absent from the data to test the missing-account check.

## Examples vs. shipped code

Anything describing a specific customer is a lesson example and is labeled as
one: `config.py` and everything in `sample_data/`. None of it ships to a
customer. Keys, `.env` files and sweep output (`reports/`, `output/`) are
git-ignored and never committed.

## Files

```
claude_backend.py           api / cli backends and the shared CLI flags
config.py                   expected accounts (lesson example)
sample_data/                snapshot of the customer's tables (lesson example)
requirements.txt            anthropic
```
