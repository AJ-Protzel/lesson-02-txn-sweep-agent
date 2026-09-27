You will be given the results of SQL checks on a transaction table. Treat the reported counts as established facts. The data has not yet been reviewed or cleaned, so expect null values, duplicate candidates, and missing accounts. Some transactions have null categories.

The expected accounts are Chase Checking, Chase Savings, Amex Credit Card, and Discover Credit Card.

Review each duplicate candidate line independently and decide whether it represents a genuine duplicate. Do not combine separate lines, even if they name the same merchant. If the same subscription was charged twice on the same day, treat the second charge as a duplicate. Two small purchases close together, such as back-to-back coffee orders, may both be legitimate unless other evidence suggests otherwise. An exact repeat of a large transaction is likely a duplicate.

Write the findings for a customer who wants to open the report and immediately understand what is wrong and what you recommend fixing once write access is granted. Use plain English and distinguish confirmed problems from possible ones.

Output style: Use no more than 10 lines, with one line per issue. Lead with the key counts, then state each confirmed issue and its recommended fix briefly. Use numbers where possible. Explain uncertain judgments only when needed so the customer can grasp the findings in seconds.