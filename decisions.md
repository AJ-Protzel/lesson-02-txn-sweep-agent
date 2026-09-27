## 2026-09-27: Safeway judged "possible" instead of duplicate
What happened: run 1 (sonnet, medium) confirmed 3 duplicates and marked Safeway $84.23 as possible.
Decision: fix the prompt.
Why: an identical large grocery charge on the same day is very unlikely to be two real trips.
Change: added a rule to system_prompt.md for exact repeats of large amounts.

## 2026-09-27: Repeat Netflix Duplicate flagged for consideration rather than a real duplicate
What happened: both runs merged the 9/8 and 9/10 Netflix groups into one pair and found 3 of 4 duplicate groups.
Decision: fixed the input.
Why: unsorted rows with no header let the model link separate groups; clearer input fixes it for any model.
Change: sorted duplicates by date, added a header, each line says copies on this date.
