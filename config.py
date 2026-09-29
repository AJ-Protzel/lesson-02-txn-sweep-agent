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

CATEGORIES = [
    "Groceries",       # Grocery store purchases and ingredients for meals
    "Dining",          # Restaurants, fast food, and other prepared meals
    "Gas",             # Fuel purchases
    "Shopping",        # Purchases that do not fit another specific category
    "Bills",           # Rent, electricity, internet, phone, and similar expenses
    "Subscriptions",   # Recurring nonessential charges, such as Netflix and Spotify
    "Health",          # Medical copays, pharmacy purchases, and healthcare expenses
    "Income",          # Money received from any source
    "Transportation",  # Flights, hotels, public transit, Uber, Lyft, and related costs
    "Transfers",       # Money moved between accounts
    "Other",           # Catchall for later recategorization during email sweeps
]