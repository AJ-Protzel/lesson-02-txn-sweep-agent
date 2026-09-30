import psycopg
from clean import url, get_merchants, categorize, write_clean
from config import CATEGORIES, CONFIRMED_DUPLICATE_IDS

runs = 9
all_pass_runs = 0
total_runs = 0

expected_map = {
    "Amazon": "Shopping",
    "Chevron": "Gas",
    "Netflix": "Subscriptions",
    "PG&E": "Bills",
    "Safeway": "Groceries",
    "Shell Gas": "Gas",
    "Spotify": "Subscriptions",
    "Starbucks": "Dining",
    "Target": "Shopping",
    "Trader Joe's": "Groceries",
}

for number in range(1, runs + 1):
    total_runs += 1
    grades = []

    category_map = categorize(get_merchants())
    write_clean(category_map)

    with psycopg.connect(url) as conn:
        map_expected = expected_map
        map_actual = dict(conn.execute("select merchant, category from tmp_category_map").fetchall())
        grade = f"run {number} map: {'PASS' if map_actual == map_expected else 'FAIL'}"
        if grade.endswith("FAIL"):
            print(grade)
        grades.append(grade)

        nulls_expected = 0
        nulls_actual = conn.execute("select count(*) from tmp_clean_transactions where category is null").fetchone()[0]
        grade = f"run {number} nulls: {'PASS' if nulls_actual == nulls_expected else 'FAIL'}"
        if grade.endswith("FAIL"):
            print(grade)
        grades.append(grade)

        categories_actual = [row[0] for row in conn.execute("select distinct category from tmp_clean_transactions").fetchall()]
        not_allowed = [category for category in categories_actual if category not in CATEGORIES]
        grade = f"run {number} allowed categories: {'PASS' if not not_allowed else 'FAIL'}"
        if grade.endswith("FAIL"):
            print(grade)
        grades.append(grade)

        mismatches_expected = 0
        mismatches_actual = conn.execute(
            """
            select count(*)
            from tmp_clean_transactions as clean
            left join tmp_category_map as map on map.merchant = clean.merchant
            where clean.category is distinct from map.category
            """
        ).fetchone()[0]
        grade = f"run {number} rows match map: {'PASS' if mismatches_actual == mismatches_expected else 'FAIL'}"
        if grade.endswith("FAIL"):
            print(grade)
        grades.append(grade)

        rows_expected = 102
        rows_actual = conn.execute("select count(*) from tmp_clean_transactions").fetchone()[0]
        dropped_actual = conn.execute("select count(*) from tmp_clean_transactions where id = any(%s)", [CONFIRMED_DUPLICATE_IDS]).fetchone()[0]
        kept_expected = [14, 60, 33, 42, 61, 81, 21]
        kept_actual = conn.execute("select count(*) from tmp_clean_transactions where id = any(%s)", [kept_expected]).fetchone()[0]
        grade = f"run {number} duplicates dropped: {'PASS' if rows_actual == rows_expected and dropped_actual == 0 and kept_actual == len(kept_expected) else 'FAIL'}"
        if grade.endswith("FAIL"):
            print(grade)
        grades.append(grade)

        changed_expected = 0
        changed_actual = conn.execute(
            """
            select count(*)
            from tmp_clean_transactions as clean
            join tmp_raw_transactions as raw on raw.id = clean.id
            where (clean.account_name, clean.txn_date, clean.merchant, clean.amount)
                  is distinct from (raw.account_name, raw.txn_date, raw.merchant, raw.amount)
            """
        ).fetchone()[0]
        grade = f"run {number} nothing else changed: {'PASS' if changed_actual == changed_expected else 'FAIL'}"
        if grade.endswith("FAIL"):
            print(grade)
        grades.append(grade)

        accounts_expected = {"Chase Checking", "Chase Savings", "Amex Credit Card"}
        accounts_actual = {row[0] for row in conn.execute("select distinct account_name from tmp_clean_transactions").fetchall()}
        grade = f"run {number} accounts: {'PASS' if accounts_actual == accounts_expected else 'FAIL'}"
        if grade.endswith("FAIL"):
            print(grade)
        grades.append(grade)

    if any(grade.endswith("FAIL") for grade in grades):
        print(category_map)
        print()
    else:
        all_pass_runs += 1

if total_runs > 0:
    print(f"{all_pass_runs}/{total_runs} runs all pass")
