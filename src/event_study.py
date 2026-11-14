"""Step 5: market-model event study (data/output/event_panel.csv).

Owner: Developer (Eric). STATUS: STUB, not implemented yet.

Inputs : transactions.csv, prices in data/raw/.
Output : config.EVENT_PANEL_CSV with exactly the columns in README.md.
Do     : events = rows with filing_date in config.V0_EVENT_START..V0_EVENT_END,
         excluding 10b5-1 trades if config.EXCLUDE_10B5_1 and trades under
         config.MIN_USD_VALUE. Day 0 is the filing date; t counts trading days.
         Estimate the market model over config.ESTIMATION_WINDOW, require
         config.MIN_ESTIMATION_DAYS valid returns, then compute ret, mkt, expected,
         AR and cumulative CAR for t in config.EVENT_WINDOW.
Checks : assert (accession, t) is unique; hand-recompute one event and match;
         run contracts.validate_event_panel on the output.

Rules: event date is the filing date; never fill data from memory (look up
file layouts in the official documentation); no hard-coded numbers (use
src/config.py); keep the contract columns in README.md exactly; log any spec you
try in specs_tried.md.
"""
import sys

import config  # noqa: F401  (all paths and parameters come from src/config.py)


def main() -> None:
    print("event_study.py: stub, not implemented yet")
    sys.exit(2)  # exit code 2 = "not implemented"; run_all.py reports it as such


if __name__ == "__main__":
    main()
