"""Step 6: routine vs opportunistic classification.

Owner: Analyst (Vincent). STATUS: STUB, not implemented yet.

Input  : data/output/transactions.csv (includes history rows from before the event window).
Output : the same file with trade_type set to routine, opportunistic or
         unclassified, then data/output/classified.flag.
Rule   : config.ROUTINE_LOOKBACK_YEARS. Routine = the insider traded in the same
         calendar month in each of the prior N years. Use only filings dated
         BEFORE the trade being classified (no look-ahead). Not enough history =
         unclassified.
Note   : v0 history is purchases only (a documented limitation; add it to
         README Threats).
Flag   : --sample runs on data/sample/ instead.

Rules: event date is the filing date; never fill data from memory (look up
file layouts in the official documentation); no hard-coded numbers (use
src/config.py); keep the contract columns in README.md exactly; log any spec you
try in specs_tried.md.
"""
import sys

import config  # noqa: F401  (all paths and parameters come from src/config.py)


def main() -> None:
    print("classify_insiders.py: stub, not implemented yet")
    sys.exit(2)  # exit code 2 = "not implemented"; run_all.py reports it as such


if __name__ == "__main__":
    main()
