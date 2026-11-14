"""Step 4: download prices and the market proxy.

Owner: Developer (Eric). STATUS: STUB, not implemented yet.

Output : daily adjusted prices for the v0_universe tickers and config.MARKET_PROXY
         in data/raw/, then data/raw/prices_done.flag.
Window : from about 400 calendar days before config.V0_EVENT_START (to cover
         config.ESTIMATION_WINDOW) to 40 days after config.V0_EVENT_END.
Rules  : yfinance only; skip files already downloaded; record the date pulled in
         DATA_SOURCES.md; report tickers with missing prices instead of dropping
         them silently.

Rules: event date is the filing date; never fill data from memory (look up
file layouts in the official documentation); no hard-coded numbers (use
src/config.py); keep the contract columns in README.md exactly; log any spec you
try in specs_tried.md.
"""
import sys

import config  # noqa: F401  (all paths and parameters come from src/config.py)


def main() -> None:
    print("fetch_prices.py: stub, not implemented yet")
    sys.exit(2)  # exit code 2 = "not implemented"; run_all.py reports it as such


if __name__ == "__main__":
    main()
