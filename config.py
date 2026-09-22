"""What the customer told us in discovery. Edit here, not in the agent."""

# The customer's database is only the tmp_ tables; nothing else is in scope.
TABLE_PREFIX = "tmp_"

# Every account the customer expects to see in their transaction data.
# Discover is deliberately absent from the seeded data to test the
# missing-account check.
EXPECTED_ACCOUNTS = [
    "Chase Checking",
    "Chase Savings",
    "Amex Credit Card",
    "Discover Credit Card",
]
