## 2026-09-27: Safeway judged "possible" instead of duplicate
What happened: run 1 (sonnet, medium) confirmed 3 duplicates and marked Safeway $84.23 as possible.
Decision: fix the prompt.
Why: an identical large grocery charge on the same day is very unlikely to be two real trips.
Change: added a rule to system_prompt.md for exact repeats of large amounts.

## 2026-09-27: Netflix groups merged into one pair
What happened: both runs merged the 9/8 and 9/10 Netflix groups into one pair and found 3 of 4 duplicate groups.
Decision: fixed the input.
Why: unsorted rows with no header let the model link separate groups; clearer input fixes it for any model.
Change: sorted duplicates by date, added a header, each line says copies on this date.

## 2026-09-27: September 8 Netflix duplicate marked "possible"  
What happened: runs 4 and 5 marked the second September 8 Netflix charge as possible instead of a duplicate.  
Decision: clarify the prompt.  
Why: two identical subscription charges on the same day should be judged as a duplicate.  
Change: added instructions to judge each candidate line individually and treat a same-day repeat subscription charge as a duplicate.

## 2026-09-27: Findings were too wordy
What happened: the model’s answers took too long to scan.
Decision: shorten the final answer.
Why: the customer should be able to see the key numbers and recommended fixes in seconds.
Change: added an output style rule to system_prompt.md to lead with counts and use short lines with minimal explanation.

## 2026-09-27: Outputs were still too wordy  
What happened: runs 6 and 7 were still too wordy.  
Decision: use a fixed output template.  
Why: the general brevity rule left too much room for lengthy explanations.  
Change: replaced the style rule with a short, one-line-per-item template.

## 2026-09-27: Safeway marked "possible" again  
What happened: run 6 marked the Safeway charge as possible instead of a duplicate.  
Decision: make the duplicate rule direct.  
Why: “likely” invited the model to hedge.  
Change: instructed the model to treat an exact repeat of a large transaction as a duplicate, matching the subscription rule.