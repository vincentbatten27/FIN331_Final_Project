"""Step 7: tables and figures for the dashboard.

Owner: Analyst (Vincent). STATUS: STUB, not implemented yet.

Inputs : transactions.csv and event_panel.csv (or data/sample/ with --sample).
Output : outputs/summary_by_trade_type.csv (trade_type, n, mean CAR, std, t-stat) and
         outputs/car_by_trade_type.png.
Rules  : CAR is the value at config.EVENT_WINDOW[1] (the sample panel is shorter:
         use the last available day and say so). Show magnitudes and n, not only
         significance. Nothing printed or plotted may be typed in by hand.

Rules: event date is the filing date; never fill data from memory (look up
file layouts in the official documentation); no hard-coded numbers (use
src/config.py); keep the contract columns in README.md exactly; log any spec you
try in specs_tried.md.
"""
import sys

import config  # noqa: F401  (all paths and parameters come from src/config.py)


def main() -> None:
    print("report.py: stub, not implemented yet")
    sys.exit(2)  # exit code 2 = "not implemented"; run_all.py reports it as such


if __name__ == "__main__":
    main()
