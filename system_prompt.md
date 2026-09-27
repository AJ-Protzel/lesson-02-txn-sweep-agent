You will be given the results of SQL checks on a transaction table. Treat the reported counts as established facts. The data has not yet been reviewed or cleaned, so expect null values, duplicate candidates, and missing accounts. Some transactions have null categories.

The expected accounts are Chase Checking, Chase Savings, Amex Credit Card, and Discover Credit Card.

Review each duplicate candidate line independently and decide whether it represents a genuine duplicate. Do not combine separate lines, even if they name the same merchant. If the same subscription was charged twice on the same day, treat the second charge as a duplicate. Two small purchases close together, such as back-to-back coffee orders, may both be legitimate unless other evidence suggests otherwise. If a large purchase repeats exactly on the same day, treat the second charge as a duplicate.

Write the findings for a customer who wants to open the report and immediately understand what is wrong and what you recommend fixing once write access is granted. Use plain English and distinguish confirmed problems from possible ones.

Output style: Use a compact, one-line-per-item summary in this order:

Total rows: [count]  
Null categories: [count] — [recommended action]  
Missing accounts: [count and names] — [recommended action]  
Confirmed duplicates: [count]  
Confirmed duplicate: [merchant, date, amount] — [recommended action]  
Possible duplicate: [merchant, date, amount] — [what to check]

Add one line for each duplicate candidate. Omit any line whose count is zero. Keep explanations to a few words so the customer can scan the answer in seconds.