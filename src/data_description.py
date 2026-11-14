"""Descriptive statistics of the final dataset.

Owner: Analyst (Vincent). STATUS: STUB, not implemented yet.

Inputs : transactions.csv and event_panel.csv (or data/sample/ with --sample).
Output : outputs/data_description.csv: first and last filing date, number of firms,
         number of purchases, counts by role and trade_type, and usd_value summary.

Rules: event date is the filing date; never fill data from memory (look up
file layouts in the official documentation); no hard-coded numbers (use
src/config.py); keep the contract columns in README.md exactly; log any spec you
try in specs_tried.md.
"""
import sys

import config  # noqa: F401  (all paths and parameters come from src/config.py)


def main() -> None:
    print("data_description.py: stub, not implemented yet")
    sys.exit(2)  # exit code 2 = "not implemented"; run_all.py reports it as such


if __name__ == "__main__":
    main()
