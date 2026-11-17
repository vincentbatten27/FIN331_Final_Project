"""Descriptive statistics of the final dataset.

Writes data_description.csv (metric, value) to outputs/ (or outputs/sample/ with --sample).
Every number is computed from the input files; nothing is typed in.
"""
import pandas as pd

import analyst_io as aio


def describe(tx: pd.DataFrame, panel: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("first_filing_date", tx["filing_date"].min().date()),
        ("last_filing_date", tx["filing_date"].max().date()),
        ("n_purchases", len(tx)),
        ("n_firms", tx["issuer_cik"].nunique()),
        ("n_insiders", tx["insider_cik"].nunique()),
        ("n_events_with_returns", panel["accession"].nunique()),
        ("n_10b5_1_trades", int(tx["is_10b5_1"].sum())),
    ]
    for role, n in tx["role"].value_counts().items():
        rows.append((f"n_role_{role}", int(n)))
    for kind, n in tx["trade_type"].value_counts().items():
        rows.append((f"n_trade_type_{kind}", int(n)))
    for stat in ("min", "median", "mean", "max"):
        rows.append((f"usd_value_{stat}", round(float(getattr(tx["usd_value"], stat)()), 2)))
    return pd.DataFrame(rows, columns=["metric", "value"])


def main() -> None:
    args = aio.parse_args(__doc__)
    tx_path, panel_path, out_dir = aio.paths(args.sample)
    aio.require(tx_path, "transactions.csv")
    aio.require(panel_path, "event_panel.csv")
    out = describe(aio.load_transactions(tx_path), aio.load_panel(panel_path))
    out_dir.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_dir / "data_description.csv", index=False)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
