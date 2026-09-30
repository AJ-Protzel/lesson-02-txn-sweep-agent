# lesson-02-txn-sweep-agent

An agent that sweeps a customer's Supabase transaction table, reports what is
wrong with it, then categorizes every merchant and builds a clean copy of the
table. Each phase is graded against answers computed by hand before any agent
code existed.

Second in a series of small agent projects; a more hands-on redo of
[lesson-01-csv-qa-agent](https://github.com/AJ-Protzel/lesson-01-csv-qa-agent).

## How it was built

Built with Claude Code, split by who did what:

- By hand: both customer calls, the eval cases and their expected answers (in
  SQL), both prompts, `sweep.py`, `test_sweep.py`, and every entry in
  `decisions.md`.
- With Claude Code, reviewed line by line: `claude_backend.py`, `clean.py`,
  `test_clean.py`.

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
| 2 | Fix what the sweep found: categorize every merchant, build a clean table | write key from the customer | done 2026-09-29 |
| 3 | Weekly wrap-up email on the database, then hand off the agent | write key | next steps |

Step 1 is read-only. Step 2 runs from a separate script with a separate key
that can write only the two tables it builds.

## Install

```bash
pip install -r requirements.txt
```

Create `.env` at the repo root with the customer's two Postgres connection
strings: a read-only key for the sweep and a write key for the clean step.

```
DATABASE_URL=postgresql://<read-only user>:<password>@<host>:5432/postgres
CLEAN_DATABASE_URL=postgresql://<write user>:<password>@<host>:5432/postgres
```

The write user can read `tmp_raw_transactions` and write only
`tmp_category_map` and `tmp_clean_transactions`.

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

```bash
python clean.py
```

Phase 2. Asks Claude to categorize each distinct merchant using
`categorize_prompt.md` and the allowed categories in `config.py`, writes the
merchant map to `tmp_category_map`, then builds `tmp_clean_transactions` from
the raw rows with the mapped category, skipping duplicates the customer
confirmed. Both tables are rewritten in one transaction on every run.

```bash
python test_clean.py
```

The phase 2 grader. Runs the clean step several times and checks the tables
against eval cases 4 to 10.

## Phase 1 results

Code finds the candidates; the model judges each duplicate candidate and
writes the report. Expected answers were computed by hand in SQL before any
agent code existed. Across the final batches, 25 of 27 runs passed all seven
checks: one was a grader bug (since fixed) and one was the model hedging on a
repeated subscription, accepted as a known limit. Every failure and fix is in
`decisions.md`.

## Phase 2 results

The model's only job is the merchant-to-category map; code does every write.
The customer confirmed one of the four duplicate groups on the second call, so
only that row is dropped and the rest wait for their statements. 14 of 14 runs
passed all seven checks across two batches. A planted wrong category was
checked to make the grader fail.

## Next steps

- Weekly wrap-up email and hand-off (step 3).
- Keep approved merchant categories and send only new merchants to Claude, so
  a category cannot change between runs.
- Drop the Netflix and Spotify duplicates once the customer confirms them.
- Reconnect Discover on the customer's side.

## What I took from building this

- Fixing the input beat fixing the prompt. The model merged two separate
  Netflix duplicate groups until the candidate lines were sorted and given a
  header; no prompt wording fixed that as cleanly.
- A word like "large" invites the model to decide for itself. The Safeway
  repeat was hedged on until code computed a Large/Small label at a fixed
  threshold and the prompt only had to apply it.
- Two of the failures were in my grader, not the model. A failing check is a
  question about the check first.
- Ship when the pass rate stops moving, not at 100%. One subscription hedge in
  27 runs survived three prompt changes, so it is recorded as a known limit.
- Give each phase only the access it needs. The sweep holds a read-only key;
  the clean step has its own key that can write two tables and nothing else.
- Let code do what code can do. The model judges duplicates and names
  categories; SQL does the counting, the joins and every write.

## Calling Claude

`claude_backend.py` gives every entry point the same two backends, as in
lesson 1:

| flag | how it calls Claude | needs |
|---|---|---|
| `--backend api` (default) | Anthropic API via the Python SDK | `ANTHROPIC_API_KEY` set; bills API credits |
| `--backend cli` | `claude -p`, Claude Code's scripting mode | Claude Code installed and logged in; uses the subscription |

Defaults are `--model claude-sonnet-5 --effort medium`. `sweep.py` and
`clean.py` currently call the `cli` backend directly. The `cli` backend runs
with no tools, no skills, MCP servers or user settings, and strips `ANTHROPIC_API_KEY` from its environment so it never
bills the API by accident.

## Sample data

`sample_data/` is a snapshot of the customer's tables. The live database has
been retired, so to run the agent, load it into your own Postgres or Supabase
project with `schema.sql`. It is generated data, not real transactions.

| file | contents |
|---|---|
| `raw_transactions.csv` | the input: 103 rows, 2026-09-02 to 2026-09-21 |
| `category_map.csv` | phase 2 output: 10 merchants and their categories |
| `clean_transactions.csv` | phase 2 output: 102 rows, categorized, confirmed duplicate removed |
| `schema.sql` | creates the three tables and the two least-access roles, and shows how to load the CSV |

Discover Credit Card is deliberately absent from the data to test the
missing-account check.

## Examples vs. shipped code

Anything describing a specific customer is a lesson example and is labeled as
one: `config.py` and everything in `sample_data/`. None of it ships to a
customer. Keys, `.env` files and sweep output (`reports/`, `output/`) are
git-ignored and never committed.

## Files

```
sweep.py                    phase 1: SQL checks, model call, findings report
test_sweep.py               grader: scores sweep reports against the eval cases
system_prompt.md            phase 1 model instructions, written by hand
clean.py                    phase 2: categorize merchants, build the clean table
test_clean.py               grader: checks the clean tables against the eval cases
categorize_prompt.md        phase 2 model instructions, written by hand
eval_cases.md               expected answers, computed by hand in SQL
decisions.md                every eval failure and what was changed
profile_raw_transactions.sql  broad read-only profile of the table
claude_backend.py           api / cli backends and the shared CLI flags
config.py                   expected accounts, categories, confirmed duplicates (lesson example)
sample_data/                snapshot of the customer's tables (lesson example)
requirements.txt            anthropic, psycopg, python-dotenv
```
