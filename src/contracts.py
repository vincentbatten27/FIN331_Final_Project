"""Column contracts for the two files passed between pipeline steps.

Mirrors the README schemas. Ask the team before changing either list.
"""
from pathlib import Path

import pandas as pd

import config

TRANSACTIONS_COLUMNS = [
    "accession", "issuer_cik", "ticker", "insider_cik", "role",
    "filing_date", "trans_date", "usd_value", "is_10b5_1", "trade_type",
]
EVENT_PANEL_COLUMNS = [
    "accession", "ticker", "filing_date", "t", "date",
    "ret", "mkt", "expected", "AR", "CAR",
]


def check_columns(df: pd.DataFrame, expected: list[str], name: str) -> list[str]:
    """Return a list of problems (empty list = file matches the contract)."""
    problems = []
    if list(df.columns) != expected:
        problems.append(f"{name}: columns {list(df.columns)} != {expected}")
    return problems


def validate_transactions(path: Path) -> list[str]:
    df = pd.read_csv(path)
    problems = check_columns(df, TRANSACTIONS_COLUMNS, path.name)
    if problems:
        return problems
    if df["accession"].duplicated().any():
        problems.append(f"{path.name}: duplicate accession rows")
    bad_role = set(df["role"]) - set(config.ROLES)
    if bad_role:
        problems.append(f"{path.name}: roles outside config.ROLES: {sorted(bad_role)}")
    bad_type = set(df["trade_type"]) - set(config.TRADE_TYPES)
    if bad_type:
        problems.append(f"{path.name}: trade_type outside config.TRADE_TYPES: {sorted(bad_type)}")
    if (pd.to_datetime(df["trans_date"]) > pd.to_datetime(df["filing_date"])).any():
        problems.append(f"{path.name}: trans_date after filing_date")
    return problems


def validate_event_panel(path: Path) -> list[str]:
    df = pd.read_csv(path)
    problems = check_columns(df, EVENT_PANEL_COLUMNS, path.name)
    if problems:
        return problems
    if (df["t"] < config.EVENT_WINDOW[0]).any() or (df["t"] > config.EVENT_WINDOW[1]).any():
        problems.append(f"{path.name}: t outside config.EVENT_WINDOW")
    if (pd.to_datetime(df["date"]) <= pd.to_datetime(df["filing_date"])).any():
        problems.append(f"{path.name}: event-window date not after filing_date")
    return problems
