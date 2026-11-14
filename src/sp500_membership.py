"""Step 3: S&P 500 membership and the v0 firm sample.

Owner: Developer (Eric).

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
import csv

import pandas as pd

import config

MEMBERSHIP_CSV = config.DATA_OUTPUT / "sp500_membership.csv"
UNIVERSE_CSV = config.DATA_OUTPUT / "v0_universe.csv"


def load_membership() -> pd.DataFrame:
    """Long table (year, ticker) from the ragged, header-less yearly file."""
    rows = []
    with open(config.SP500_YEARLY_CSV, newline="") as f:
        for line in csv.reader(f):
            if not line or not line[0].strip():
                continue
            year = int(line[0])
            rows += [(year, t.strip().upper()) for t in line[1:] if t.strip()]
    df = pd.DataFrame(rows, columns=["year", "ticker"]).drop_duplicates()
    return df.sort_values(["year", "ticker"]).reset_index(drop=True)


def draw_universe(membership: pd.DataFrame) -> pd.DataFrame:
    """config.V0_N_FIRMS tickers drawn with config.SEED from the Jan-1 list of the
    v0 event year. Sorted first so the draw depends only on the list and the seed."""
    year = config.V0_EVENT_START.year
    pool = membership.loc[membership["year"] == year, "ticker"].sort_values().reset_index(drop=True)
    if len(pool) < config.V0_N_FIRMS:
        raise SystemExit(f"Only {len(pool)} tickers listed for {year}; need {config.V0_N_FIRMS}.")
    picked = pool.sample(n=config.V0_N_FIRMS, random_state=config.SEED).sort_values()
    return pd.DataFrame({"year": year, "ticker": picked.values})


def main() -> None:
    config.DATA_OUTPUT.mkdir(parents=True, exist_ok=True)
    membership = load_membership()
    universe = draw_universe(membership)
    membership.to_csv(MEMBERSHIP_CSV, index=False)
    universe.to_csv(UNIVERSE_CSV, index=False)
    counts = membership.groupby("year").size()
    print(f"sp500_membership.csv: {len(membership)} rows, years {counts.index.min()}-{counts.index.max()} "
          f"({counts.min()}-{counts.max()} tickers per year)")
    print(f"v0_universe.csv: {len(universe)} tickers from the Jan-1-{universe['year'].iloc[0]} list "
          f"(seed {config.SEED}): {', '.join(universe['ticker'])}")


if __name__ == "__main__":
    main()
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
