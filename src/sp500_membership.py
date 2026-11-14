"""Step 3: S&P 500 membership and the v0 firm sample.

Owner: Developer (Eric). STATUS: STUB, not implemented yet.

Input  : config.SP500_YEARLY_CSV (one row per year, first column is the year, the
         rest are tickers as of Jan 1; no header).
Output : data/output/sp500_membership.csv (year, ticker) and
         data/output/v0_universe.csv: config.V0_N_FIRMS tickers drawn with
         config.SEED from the list as of Jan 1 of config.V0_EVENT_START's year.
Do     : membership for an event is the list for that event's year (as of Jan 1).
         Never pick tickers by hand or from memory.
Note   : Jan-1 snapshots miss mid-year changes; say so in README Threats.

Rules: event date is the filing date; never fill data from memory (look up
file layouts in the official documentation); no hard-coded numbers (use
src/config.py); keep the contract columns in README.md exactly; log any spec you
try in specs_tried.md.
"""
import sys

import config  # noqa: F401  (all paths and parameters come from src/config.py)


def main() -> None:
    print("sp500_membership.py: stub, not implemented yet")
    sys.exit(2)  # exit code 2 = "not implemented"; run_all.py reports it as such


if __name__ == "__main__":
    main()
