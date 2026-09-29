from sweep import run_sweep

replies = run_sweep(runs=9)
all_pass_runs = 0
total_runs = 0

for number, reply in enumerate(replies, start=1):
    total_runs += 1
    grades = []

    rows_expected = "Total rows: 103"
    grade = f"run {number} rows: {'PASS' if rows_expected in reply else 'FAIL'}"
    if grade.endswith("FAIL"):
        print(grade)
    grades.append(grade)

    nulls_expected = "Null categories: 23"
    grade = f"run {number} nulls: {'PASS' if nulls_expected in reply else 'FAIL'}"
    if grade.endswith("FAIL"):
        print(grade)
    grades.append(grade)

    accounts_num_expected = "Missing accounts: 1"
    accounts_acc_expected = "Discover Credit Card"
    grade = f"run {number} accounts: {'PASS' if accounts_num_expected in reply and accounts_acc_expected in reply else 'FAIL'}"
    if grade.endswith("FAIL"):
        print(grade)
    grades.append(grade)

    c_duplicates_total_expected = "Confirmed duplicates: 4"
    grade = f"run {number} c_duplicates_total: {'PASS' if c_duplicates_total_expected in reply else 'FAIL'}"
    if grade.endswith("FAIL"):
        print(grade)
    grades.append(grade)

    expected_duplicates = [
        ("Netflix", "2026-09-08", "$15.49"),
        ("Netflix", "2026-09-10", "$15.49"),
        ("Spotify", "2026-09-21", "$11.99"),
        ("Safeway", "2026-09-14", "$84.23"),
    ]

    confirmed_count = 0
    matched = set()

    for line in reply.splitlines():
        line_lower = line.strip().lower()

        if line_lower.startswith("confirmed duplicate:"):
            confirmed_count += 1

            for duplicate in expected_duplicates:
                if all(part.lower() in line_lower for part in duplicate):
                    matched.add(duplicate)

    grade = f"run {number} confirmed count: {'PASS' if confirmed_count == 4 else 'FAIL'}"
    if grade.endswith("FAIL"):
        print(grade)
    grades.append(grade)

    grade = f"run {number} matched duplicates: {'PASS' if len(matched) == 4 else 'FAIL'}"
    if grade.endswith("FAIL"):
        print(grade)
    grades.append(grade)

    p_duplicates_expected = "Possible duplicate"
    grade = f"run {number} p_duplicates: {'PASS' if p_duplicates_expected not in reply else 'FAIL'}"
    if grade.endswith("FAIL"):
        print(grade)
    grades.append(grade)

    if any(grade.endswith("FAIL") for grade in grades):
        print(reply)
        print()
    else:
        all_pass_runs += 1

if total_runs > 0:
    print(f"{all_pass_runs}/{total_runs} runs all pass")