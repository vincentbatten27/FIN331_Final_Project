# Data sources and provenance

One row per raw input. Fill in a row when you first pull the data.
Raw files live in `data/raw/` (git-ignored); the code in the last column recreates them.

| Input | Source (URL) | Date pulled | Used for | Where it lives | Code that gets it |
|---|---|---|---|---|---|
| SEC insider transactions data sets (quarterly zips) | | | Form 4 purchases | `data/raw/` | `src/fetch_sec.py` |
| Yearly S&P 500 constituents as of Jan 1 | provided by the team (not re-downloadable) | 2026-11-13 | S&P 500 membership | `data/reference/spx_yearly_tickers.csv` (committed) | none |
| Wikipedia S&P 500 changes table | | | membership between Jan-1 snapshots (if used) | `data/raw/` | `src/sp500_membership.py` |
| Stock and SPY prices (yfinance) | | | returns, market proxy | `data/raw/` | `src/fetch_prices.py` |
| Ken French factors | | | robustness (if used) | `data/raw/` | `src/fetch_prices.py` |
