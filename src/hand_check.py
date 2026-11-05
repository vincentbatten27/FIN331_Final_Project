"""Hand-check stub: draw a reproducible random sample of purchases to verify by hand.

Planned behavior (not implemented yet):
  1. Read config.TRANSACTIONS_CSV.
  2. Draw N rows with config.SEED.
  3. Write them to audits/ with an EDGAR filing-index link built from
     accession + issuer_cik, plus blank columns for the checker to fill in
     (filing_date matches? usd_value matches? is_10b5_1 matches? duplicate?).
Record findings in audits/<date>_hand_check.md.
"""
import config  # noqa: F401


def main() -> None:
    raise NotImplementedError("hand_check is a stub; implement after transactions.csv exists")


if __name__ == "__main__":
    main()
