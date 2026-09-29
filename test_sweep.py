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
    
    c_duplicates_expected = "Confirmed duplicates: 4"
    print(f"run {number} c_duplicates: {'PASS' if c_duplicates_expected in reply else 'FAIL'}")

    p_duplicates_expected = "Possible duplicate"
    print(f"run {number} p_duplicates: {'PASS' if p_duplicates_expected not in reply else 'FAIL'}")