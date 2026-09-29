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
| 1 | Sweep the table: find data errors, check every expected account is present | read-only key | done 2026-09-29 |
| 2 | Fix what the sweep found | write key from the customer | next |
| 3 | Weekly wrap-up email on the database, then hand off the agent | write key | not started |

Step 1 is read-only. Nothing is written to the customer's database until they
hand over a write key.

## Install

```bash
pip install -r requirements.txt
```

Create `.env` at the repo root with a read-only Postgres connection string
(the customer's read-only key):

```
DATABASE_URL=postgresql://<read-only user>:<password>@<host>:5432/postgres
```

## Run

```bash
python sweep.py
```

Runs the three checks in SQL (null categories, missing accounts, duplicate
candidates), sends the results to Claude with `system_prompt.md`, and prints
two findings reports.

```bash
python test_sweep.py
```

The grader. Runs the sweep several times and checks each report against the
hand-computed answers in `eval_cases.md`, then prints how many runs passed
every check.

## Phase 1 results

Code finds the candidates; the model judges each duplicate candidate and
writes the report. Expected answers were computed by hand in SQL before any
agent code existed. Across the final batches, 25 of 27 runs passed all seven
checks: one was a grader bug (since fixed) and one was the model hedging on a
repeated subscription, accepted as a known limit. Every failure and fix is in
`decisions.md`.

## Calling Claude

`claude_backend.py` gives every entry point the same two backends, as in
lesson 1:

| flag | how it calls Claude | needs |
|---|---|---|
| `--backend api` (default) | Anthropic API via the Python SDK | `ANTHROPIC_API_KEY` set; bills API credits |
| `--backend cli` | `claude -p`, Claude Code's scripting mode | Claude Code installed and logged in; uses the subscription |

Defaults are `--model claude-sonnet-5 --effort medium`. `sweep.py` currently
calls the `cli` backend directly. The `cli` backend runs
with no tools, no skills, MCP servers or user settings, and strips `ANTHROPIC_API_KEY` from its environment so it never
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
sweep.py                    the agent: SQL checks, model call, findings report
test_sweep.py               grader: scores sweep reports against the eval cases
system_prompt.md            the model's instructions, written by hand
eval_cases.md               expected answers, computed by hand in SQL
decisions.md                every eval failure and what was changed
profile_raw_transactions.sql  broad read-only profile of the table
claude_backend.py           api / cli backends and the shared CLI flags
config.py                   expected accounts (lesson example)
sample_data/                snapshot of the customer's tables (lesson example)
requirements.txt            anthropic, psycopg, python-dotenv
```
