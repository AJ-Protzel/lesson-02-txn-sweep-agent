## 2026-09-27: Safeway judged "possible" instead of duplicate
What happened: run 1 (sonnet, medium) confirmed 3 duplicates and marked Safeway $84.23 as possible.
Decision: fix the prompt.
Why: an identical large grocery charge on the same day is very unlikely to be two real trips.
Change: added a rule to system_prompt.md for exact repeats of large amounts.