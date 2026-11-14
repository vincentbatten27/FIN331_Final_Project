# Data sources and provenance

One row per raw input. Fill in a row when you first pull the data.
Raw files live in `data/raw/` (git-ignored); the code in the last column recreates them.

| Input | Source (URL) | Date pulled | Used for | Where it lives | Code that gets it |
|---|---|---|---|---|---|
| SEC insider transactions data sets (quarterly zips, 2018q1-2021q2) | https://www.sec.gov/data-research/sec-markets-data/insider-transactions-data-sets (zip links read from this page) | 2026-11-14 | Form 4 purchases | `data/raw/<YYYY>q<N>_form345.zip` | `src/fetch_sec.py` |
| SEC data set documentation (table and field definitions) | https://www.sec.gov/files/insider_transactions_readme.pdf | 2026-11-14 | field names used in `src/build_transactions.py` | `data/raw/docs/insider_transactions_readme.pdf` | `src/fetch_sec.py` |
| Yearly S&P 500 constituents as of Jan 1 | provided by the team (not re-downloadable) | 2026-11-13 | S&P 500 membership | `data/reference/spx_yearly_tickers.csv` (committed) | none |
| Wikipedia S&P 500 changes table | not used in v0 (membership = Jan-1 list of the event year) | | membership between Jan-1 snapshots (if used) | `data/raw/` | `src/sp500_membership.py` |
| Stock and SPY prices (yfinance, adjusted close) | Yahoo Finance via the `yfinance` package | 2026-11-14 | returns, market proxy | `data/raw/prices/<ticker>.csv` | `src/fetch_prices.py` |
| Ken French factors | not used in v0 | | robustness (if used) | `data/raw/` | `src/fetch_prices.py` |
