"""Step 2: build the purchase table (data/output/transactions.csv).

Owner: Developer (Eric). STATUS: STUB, not implemented yet.

Inputs : the zips in data/raw/, data/output/v0_universe.csv (step 3).
Output : config.TRANSACTIONS_CSV with exactly the columns in README.md.
Do     : keep open-market purchases only (config.TRANSACTION_CODE), insiders whose
         role is in config.ROLES, filing dates from config.V0_HISTORY_START to
         config.V0_EVENT_END (history rows are needed by the routine rule). Dedupe
         by accession. Take filing_date from the filing, not the trade.
         Set is_10b5_1 from the filing's own flag. Write trade_type = "unclassified"
         (the Analyst fills it in step 6). usd_value = shares x price.
Checks : assert accession is unique; assert trans_date <= filing_date;
         run contracts.validate_transactions on the output.

Rules: event date is the filing date; never fill data from memory (look up
file layouts in the official documentation); no hard-coded numbers (use
src/config.py); keep the contract columns in README.md exactly; log any spec you
try in specs_tried.md.
"""
import sys

import config  # noqa: F401  (all paths and parameters come from src/config.py)


def main() -> None:
    print("build_transactions.py: stub, not implemented yet")
    sys.exit(2)  # exit code 2 = "not implemented"; run_all.py reports it as such


if __name__ == "__main__":
    main()
