"""Test run: the v0 spec on every S&P 500 firm instead of V0_N_FIRMS (audit A2, step 1).

Run from the repo root:   python dev/test_all_firms.py

Same code and settings as the pipeline, with two overrides made in memory only:
  * V0_N_FIRMS = every ticker on the Jan-1 list of the v0 event year;
  * pipeline files go to data/temp/all_firms_test/, so src/config.py and the
    committed contract files in data/output/ are never changed.
Downloads only what is missing (SEC zips, prices) into data/raw/.

Writes dev/all_firms_test/:
  summary_by_trade_type.csv  report.summarize() on the test events
  summary_by_role.csv        the same statistics by CEO / CFO
  trade_types_by_year.csv    classifier labels by filing year (all purchases)
  coverage.csv               how many purchases survive each step, and why not
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import config  # noqa: E402

WORK = config.DATA_TEMP / "all_firms_test"
RESULTS = Path(__file__).resolve().parent / "all_firms_test"
config.DATA_OUTPUT = WORK
config.TRANSACTIONS_CSV = WORK / "transactions.csv"
config.EVENT_PANEL_CSV = WORK / "event_panel.csv"

import analyst_io  # noqa: E402
import build_transactions  # noqa: E402
import classify_insiders  # noqa: E402
import event_study  # noqa: E402
import fetch_prices  # noqa: E402
import fetch_sec  # noqa: E402
import report  # noqa: E402
import sp500_membership  # noqa: E402

fetch_prices.FLAG = WORK / "prices_done.flag"


def by_role(events: pd.DataFrame) -> pd.DataFrame:
    """report.summarize() grouped by role instead of trade_type."""
    out = report.summarize(events.assign(trade_type=events["role"]))
    return out.rename(columns={"trade_type": "role"})


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)

    membership = sp500_membership.load_membership()
    config.V0_N_FIRMS = int((membership["year"] == config.V0_EVENT_START.year).sum())
    sp500_membership.main()
    fetch_sec.main()
    build_transactions.main()
    fetch_prices.main()
    event_study.main()

    tx = analyst_io.load_transactions(config.TRANSACTIONS_CSV)
    tx["trade_type"] = classify_insiders.classify(tx, config.ROUTINE_LOOKBACK_YEARS,
                                                  config.V0_HISTORY_START)
    panel = analyst_io.load_panel(config.EVENT_PANEL_CSV)
    events = analyst_io.event_car(tx, panel)

    report.summarize(events).to_csv(RESULTS / "summary_by_trade_type.csv", index=False)
    by_role(events).to_csv(RESULTS / "summary_by_role.csv", index=False)
    (tx.assign(filing_year=tx["filing_date"].dt.year)
       .pivot_table(index="filing_year", columns="trade_type", values="accession",
                    aggfunc="count", fill_value=0)
       .reset_index()
       .to_csv(RESULTS / "trade_types_by_year.csv", index=False))

    universe = set(pd.read_csv(sp500_membership.UNIVERSE_CSV)["ticker"])
    in_window = tx[tx["filing_date"].between(pd.Timestamp(config.V0_EVENT_START),
                                             pd.Timestamp(config.V0_EVENT_END))]
    eligible = event_study.select_events(in_window)
    no_prices = sorted(t for t in universe if not fetch_prices.price_path(t).exists())
    no_cik = sorted(universe - set(build_transactions.issuer_ciks()))
    coverage = pd.DataFrame([
        ("firms_on_jan1_list", len(universe)),
        ("firms_without_filings_in_event_window", len(no_cik)),
        ("firms_without_yfinance_prices", len(no_prices)),
        ("purchases_filed_in_event_window", len(in_window)),
        ("purchases_passing_size_and_10b5_1_filters", len(eligible)),
        ("events_with_returns", panel["accession"].nunique()),
        ("events_dropped_no_prices", int(eligible["ticker"].isin(no_prices).sum())),
        ("unique_firm_filing_days", len(events.drop_duplicates(["ticker", "filing_date"]))),
        ("tickers_without_filings", " ".join(no_cik)),
        ("tickers_without_prices", " ".join(no_prices)),
    ], columns=["metric", "value"])
    coverage.to_csv(RESULTS / "coverage.csv", index=False)

    print("\n" + coverage.head(8).to_string(index=False))
    print("\n" + pd.read_csv(RESULTS / "summary_by_trade_type.csv").to_string(index=False))
    print(f"\nresults in {RESULTS.relative_to(config.ROOT)}/")


if __name__ == "__main__":
    main()
