from sweep import run_sweep

replies = run_sweep()

for number, reply in enumerate(replies, start=1):
    print(reply)

    rows_expected = "Total rows: 103"
    print(f"run {number} rows: {'PASS' if rows_expected in reply else 'FAIL'}")
    
    nulls_expected = "Null categories: 23"
    print(f"run {number} nulls: {'PASS' if nulls_expected in reply else 'FAIL'}")

    accounts_num_expected = "Missing accounts: 1"
    accounts_acc_expected = "Discover Credit Card"
    print(f"run {number} accounts: {'PASS' if accounts_num_expected in reply and accounts_acc_expected in reply else 'FAIL'}")
    
    c_duplicates_total_expected = "Confirmed duplicates: 4"
    print(f"run {number} c_duplicates_total: {'PASS' if c_duplicates_total_expected in reply else 'FAIL'}")

    expected_duplicates = [
        ("Netflix", "2026-09-08", "$15.49"),
        ("Netflix", "2026-09-10", "$15.49"),
        ("Spotify", "2026-09-21", "$11.99"),
        ("Safeway", "2026-09-14", "$84.23"),
    ]

    confirmed_count = 0
    matched = set()

    for line in reply.splitlines():
        if line.strip().startswith("Confirmed duplicate:"):
            confirmed_count += 1

            for duplicate in expected_duplicates:
                if all(part in line for part in duplicate):
                    matched.add(duplicate)

    print(f"run {number} confirmed count: {'PASS' if confirmed_count == 4 else 'FAIL'}")

    print(f"run {number} matched duplicates: {'PASS' if len(matched) == 4 else 'FAIL'}")

    p_duplicates_expected = "Possible duplicate"
    print(f"run {number} p_duplicates: {'PASS' if p_duplicates_expected not in reply else 'FAIL'}")