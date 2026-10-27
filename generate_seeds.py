"""Generate synthetic source-system CSVs for the dbt practice project.

All data is fake. Four "source systems" describe the same clients with
different ID formats and column names, so you have a real job to do when
you conform them into one canonical party table.

Usage:
    python generate_seeds.py                 # clean data -> ./seeds
    python generate_seeds.py --out seeds     # choose output folder
    python generate_seeds.py --messy         # add duplicates, orphans, nulls
"""
import argparse
import csv
import random
from datetime import date, timedelta
from pathlib import Path

FIRST = ["Amara", "Ben", "Chloe", "Daniel", "Esme", "Femi", "Grace", "Hugo",
         "Imani", "Jack", "Kira", "Leo", "Maya", "Noah", "Olivia", "Priya",
         "Quentin", "Ravi", "Sofia", "Tom", "Uma", "Victor", "Willow", "Zane"]
LAST = ["Adams", "Bennett", "Clarke", "Dawson", "Edwards", "Foster", "Grant",
        "Hughes", "Iqbal", "Jones", "Khan", "Lewis", "Morgan", "Nelson",
        "Owens", "Patel", "Reid", "Singh", "Taylor", "Walker"]
SEGMENTS = ["Private Banking", "Wealth Management", "Premier"]
SAVINGS_PRODUCTS = ["Easy Access", "Fixed Term 12m", "Notice 90 Day", "ISA"]


def rand_date(rng, start_year=2005, end_year=2025):
    start = date(start_year, 1, 1)
    span = (date(end_year, 12, 31) - start).days
    return (start + timedelta(days=rng.randint(0, span))).isoformat()


def write_csv(path, header, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="seeds")
    ap.add_argument("--clients", type=int, default=300)
    ap.add_argument("--messy", action="store_true",
                    help="add duplicates, orphan accounts and null balances")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    party, current, savings, mortgages = [], [], [], []
    acct_n = 1000

    for i in range(1, args.clients + 1):
        # Source 1 (CRM): ID looks like P000123
        party.append([
            f"P{i:06d}",
            f"{rng.choice(FIRST)} {rng.choice(LAST)}",
            rand_date(rng, 1945, 1995),
            rng.choice(SEGMENTS),
            f"N{rng.randint(1, 22)} {rng.randint(1, 9)}{rng.choice('ABDEFGHJLNPQRSTUWXYZ')}"
            f"{rng.choice('ABDEFGHJLNPQRSTUWXYZ')}",
        ])

        # Source 2 (current accounts): customer_no looks like C-000123
        if rng.random() < 0.90:
            acct_n += 1
            current.append([
                f"CA{acct_n}",
                f"C-{i:06d}",
                rand_date(rng),
                round(rng.uniform(-2000, 60000), 2),
                rng.choice(["OPEN", "OPEN", "OPEN", "DORMANT"]),
            ])

        # Source 3 (savings): cust_id is a bare number with no padding
        if rng.random() < 0.60:
            for _ in range(rng.choice([1, 1, 2])):
                acct_n += 1
                savings.append([
                    f"SV{acct_n}",
                    str(i),
                    rng.choice(SAVINGS_PRODUCTS),
                    round(rng.uniform(1000, 250000), 2),
                    rand_date(rng),
                ])

        # Source 4 (mortgages): party_id is lowercase, like p000123
        if rng.random() < 0.35:
            acct_n += 1
            mortgages.append([
                f"MG{acct_n}",
                f"p{i:06d}",
                round(rng.uniform(50000, 900000), 2),
                round(rng.uniform(1.5, 6.5), 2),
                rand_date(rng, 2012, 2025),
            ])

    if args.messy:
        # Duplicate client in CRM (same party_ref twice)
        party.append(list(party[0]))
        party.append(list(party[1]))
        # Orphan accounts pointing at clients that do not exist
        savings.append(["SV9001", "99991", "Easy Access", 12000.00, "2020-05-01"])
        mortgages.append(["MG9001", "p999992", 250000.00, 4.1, "2019-03-12"])
        current.append(["CA9001", "C-999993", "2018-07-09", 800.00, "OPEN"])
        # Null balances
        for rows, col in ((current, 3), (savings, 3), (mortgages, 2)):
            rows[rng.randrange(len(rows))][col] = ""

    write_csv(out / "src_crm_party.csv",
              ["party_ref", "full_name", "dob", "segment", "postcode"], party)
    write_csv(out / "src_current_accounts.csv",
              ["account_no", "customer_no", "open_date", "balance", "status"], current)
    write_csv(out / "src_savings.csv",
              ["acct_id", "cust_id", "product_name", "balance_gbp", "opened"], savings)
    write_csv(out / "src_mortgages.csv",
              ["mortgage_id", "party_id", "outstanding_balance", "rate_pct", "start_date"],
              mortgages)

    print(f"party={len(party)} current={len(current)} "
          f"savings={len(savings)} mortgages={len(mortgages)} -> {out}/")


if __name__ == "__main__":
    main()