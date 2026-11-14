"""Hand check: draw a reproducible random sample of purchases to verify by hand.

Writes hand_check_sample.csv with the sampled rows, an EDGAR folder link built from
issuer_cik + accession, and blank columns for the checker to fill in:
  filing_date_ok, usd_value_ok, is_10b5_1_ok, duplicate_found, notes
Real run : reads data/output/transactions.csv, writes audits/hand_check_sample.csv.
--sample : reads data/sample/, writes data/temp/hand_check_sample_FAKE.csv.
Verify the EDGAR URL pattern once by opening a link before trusting it.
Record what you found in audits/<date>_hand_check.md.
"""
import argparse

import pandas as pd

import analyst_io as aio
import config

N_DEFAULT = 10


def edgar_url(issuer_cik: int, accession: str) -> str:
    return f"https://www.sec.gov/Archives/edgar/data/{int(issuer_cik)}/{accession.replace('-', '')}/"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--sample", action="store_true")
    ap.add_argument("--n", type=int, default=N_DEFAULT, help="rows to draw")
    args = ap.parse_args()
    tx_path, _, _ = aio.paths(args.sample)
    aio.require(tx_path, "transactions.csv")
    tx = aio.load_transactions(tx_path)
    drawn = tx.sample(n=min(args.n, len(tx)), random_state=config.SEED).sort_values("filing_date").copy()
    drawn["edgar_url"] = [edgar_url(c, a) for c, a in zip(drawn["issuer_cik"], drawn["accession"])]
    for col in ("filing_date_ok", "usd_value_ok", "is_10b5_1_ok", "duplicate_found", "notes"):
        drawn[col] = ""
    if args.sample:
        config.DATA_TEMP.mkdir(parents=True, exist_ok=True)
        out = config.DATA_TEMP / "hand_check_sample_FAKE.csv"
    else:
        out = config.AUDITS / "hand_check_sample.csv"
    drawn.to_csv(out, index=False)
    print(f"wrote {len(drawn)} rows to {out}")


if __name__ == "__main__":
    main()
