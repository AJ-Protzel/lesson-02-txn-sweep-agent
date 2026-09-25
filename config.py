"""LESSON EXAMPLE ONLY. Not shipped to the customer.

Sample discovery answers used to develop and test this agent. A real deployment
supplies its own values; nothing here is customer data.
"""

# Every account the customer expects to see in their transaction data.
# Discover is deliberately absent from the seeded data to test the
# missing-account check.
EXPECTED_ACCOUNTS = [
    "Chase Checking",
    "Chase Savings",
    "Amex Credit Card",
    "Discover Credit Card",
]
