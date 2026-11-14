"""Step 6: routine vs opportunistic classification (Cohen, Malloy & Pomorski 2012).

Rule (proposed; see specs_tried.md):
  * A purchase is ROUTINE if the insider also bought in the same calendar month in
    each of the prior config.ROUTINE_LOOKBACK_YEARS years.
  * Otherwise OPPORTUNISTIC.
  * UNCLASSIFIED if the data does not reach back far enough (the lookback window
    starts before config.V0_HISTORY_START), so we cannot tell.
No look-ahead: only purchases whose FILING date is strictly before the current
purchase's filing date are used as history.
v0 limitation: history is purchases only (the transactions file holds no sales).

Real run : reads data/output/transactions.csv, rewrites its trade_type column, then
           writes data/output/classified.flag.
--sample : reads data/sample/, writes data/temp/transactions_classified_sample.csv
           (the sample files are never modified).
"""
import pandas as pd

import analyst_io as aio
import config


def classify(tx: pd.DataFrame, lookback_years: int, history_start) -> pd.Series:
    """Return a trade_type Series aligned with tx.index."""
    history_start = pd.Timestamp(history_start)
    months_by_insider = {
        cik: g[["filing_date", "trans_date"]] for cik, g in tx.groupby("insider_cik")
    }
    labels = {}
    for idx, row in tx.iterrows():
        window_start = row["trans_date"] - pd.DateOffset(years=lookback_years)
        if window_start < history_start:
            labels[idx] = "unclassified"
            continue
        g = months_by_insider[row["insider_cik"]]
        past = g[g["filing_date"] < row["filing_date"]]  # strictly earlier filings only
        seen = set(zip(past["trans_date"].dt.year, past["trans_date"].dt.month))
        year, month = row["trans_date"].year, row["trans_date"].month
        routine = all((year - k, month) in seen for k in range(1, lookback_years + 1))
        labels[idx] = "routine" if routine else "opportunistic"
    return pd.Series(labels, name="trade_type")


def main() -> None:
    args = aio.parse_args(__doc__)
    tx_path, _, _ = aio.paths(args.sample)
    aio.require(tx_path, "transactions.csv")
    tx = aio.load_transactions(tx_path)
    tx["trade_type"] = classify(tx, config.ROUTINE_LOOKBACK_YEARS, config.V0_HISTORY_START)
    print(tx["trade_type"].value_counts().to_string())
    if args.sample:
        config.DATA_TEMP.mkdir(parents=True, exist_ok=True)
        tx.to_csv(config.DATA_TEMP / "transactions_classified_sample.csv", index=False)
    else:
        tx.to_csv(config.TRANSACTIONS_CSV, index=False)
        (config.DATA_OUTPUT / "classified.flag").write_text("done\n")


if __name__ == "__main__":
    main()
