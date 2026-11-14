"""Shared input/output helpers for the Analyst scripts (Vincent).

Real runs read data/output/ and write to outputs/.
--sample runs read data/sample/ (fake rows) and write to outputs/sample/, so fake
numbers can never be mistaken for real results.
"""
import argparse
import sys
from pathlib import Path

import pandas as pd

import config

NOT_READY = 2  # same exit code the stubs use; run_all.py reports it as "not implemented"


def parse_args(description: str) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=description)
    ap.add_argument("--sample", action="store_true", help="use data/sample/ and write to outputs/sample/")
    return ap.parse_args()


def paths(sample: bool) -> tuple[Path, Path, Path]:
    """(transactions csv, event panel csv, output dir)."""
    if sample:
        return config.SAMPLE_TRANSACTIONS_CSV, config.SAMPLE_EVENT_PANEL_CSV, config.OUTPUTS / "sample"
    return config.TRANSACTIONS_CSV, config.EVENT_PANEL_CSV, config.OUTPUTS


def require(path: Path, what: str) -> None:
    """Exit with 'not ready' if an upstream file does not exist yet."""
    if not path.exists():
        print(f"{what} not found at {path}; waiting for the upstream step.")
        sys.exit(NOT_READY)


def load_transactions(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, parse_dates=["filing_date", "trans_date"])


def load_panel(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, parse_dates=["filing_date", "date"])


def event_car(tx: pd.DataFrame, panel: pd.DataFrame) -> pd.DataFrame:
    """One row per purchase that has event-panel data, with its CAR.

    CAR is taken at t = config.EVENT_WINDOW[1] when present, otherwise at the
    last available t (the sample panel is shorter). `t_used` records which.
    Filters from config: size filter and, if config.EXCLUDE_10B5_1, 10b5-1 trades.
    """
    last = panel.sort_values("t").groupby("accession").tail(1)[["accession", "t", "CAR"]]
    last = last.rename(columns={"t": "t_used"})
    out = tx.merge(last, on="accession", how="inner", validate="one_to_one")
    out = out[out["usd_value"] >= config.MIN_USD_VALUE]
    if config.EXCLUDE_10B5_1:
        out = out[out["is_10b5_1"] == 0]
    return out.reset_index(drop=True)
