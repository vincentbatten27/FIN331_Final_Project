"""Explore page. Owner: Product manager (David).

Filters (trade type, role, include 10b5-1, filing-date range) over transactions.csv
joined to event-panel CAR. Reads data/output/ when both contract files exist,
otherwise data/sample/ with a visible SAMPLE DATA warning.
Rules: read only from data/output/, outputs/ or data/sample/; no downloads or model
fitting here; no hard-coded numbers (window and roles come from src/config.py).
"""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import config  # noqa: E402

st.set_page_config(page_title="Explore", layout="wide")
st.title("Explore")

USING_SAMPLE = not (config.TRANSACTIONS_CSV.exists() and config.EVENT_PANEL_CSV.exists())
TX_PATH = config.SAMPLE_TRANSACTIONS_CSV if USING_SAMPLE else config.TRANSACTIONS_CSV
PANEL_PATH = config.SAMPLE_EVENT_PANEL_CSV if USING_SAMPLE else config.EVENT_PANEL_CSV

START, END = config.EVENT_WINDOW
CAR_FULL = f"car_{START}_{END}"
FULL_LABEL = f"CAR[+{START},+{END}]"

if USING_SAMPLE:
    st.warning(
        f"SAMPLE DATA: fake rows from {config.DATA_SAMPLE.relative_to(config.ROOT).as_posix()}/. "
        "Not real results. Real data appears here once the pipeline writes data/output/."
    )


@st.cache_data
def load(tx_path: str, panel_path: str) -> pd.DataFrame:
    """One row per purchase with CAR over the full event window and CAR to date."""
    tx = pd.read_csv(tx_path, parse_dates=["filing_date", "trans_date"])
    panel = pd.read_csv(panel_path, parse_dates=["filing_date", "date"])
    panel = panel[panel["t"].between(START, END)]

    # CAR over the full window: only for events whose panel reaches the last day.
    full = panel.loc[panel["t"] == END, ["accession", "CAR"]].rename(columns={"CAR": CAR_FULL})
    # CAR to the last available day in the window (for events still in progress
    # or with a short panel); keep the day so the horizon is always visible.
    last = (panel.sort_values("t").groupby("accession").tail(1)[["accession", "t", "CAR"]]
            .rename(columns={"t": "car_last_day", "CAR": "car_to_date"}))
    return tx.merge(full, on="accession", how="left").merge(last, on="accession", how="left")


df = load(str(TX_PATH), str(PANEL_PATH))

# ---- Filters -----------------------------------------------------------------
c1, c2, c3 = st.columns(3)
types = c1.multiselect("Trade type", config.TRADE_TYPES, default=config.TRADE_TYPES)
roles = c2.multiselect("Role", config.ROLES, default=config.ROLES)
include_10b5_1 = c3.checkbox(
    "Include 10b5-1 trades", value=not config.EXCLUDE_10B5_1,
    help="10b5-1 trades are pre-planned, so they carry little private information. "
         "The main spec excludes them.",
)

dmin, dmax = df["filing_date"].min().date(), df["filing_date"].max().date()
dates = st.slider("Filing date (the event date)", min_value=dmin, max_value=dmax,
                  value=(dmin, dmax), format="YYYY-MM-DD")

view = df[
    df["trade_type"].isin(types)
    & df["role"].isin(roles)
    & df["filing_date"].dt.date.between(*dates)
]
if not include_10b5_1:
    view = view[view["is_10b5_1"] == 0]

# ---- Table -------------------------------------------------------------------
st.subheader(f"Purchases ({len(view)})")
cols = ["accession", "ticker", "role", "filing_date", "trans_date", "usd_value",
        "is_10b5_1", "trade_type", CAR_FULL, "car_to_date", "car_last_day"]
st.dataframe(
    view[cols].sort_values("filing_date", ascending=False),
    width="stretch",
    hide_index=True,
    column_config={
        "filing_date": st.column_config.DateColumn("filing_date", format="YYYY-MM-DD"),
        "trans_date": st.column_config.DateColumn("trans_date", format="YYYY-MM-DD"),
        "usd_value": st.column_config.NumberColumn("usd_value", format="$%,.0f"),
        CAR_FULL: st.column_config.NumberColumn(FULL_LABEL, format="percent"),
        "car_to_date": st.column_config.NumberColumn("CAR to date", format="percent"),
        "car_last_day": st.column_config.NumberColumn("CAR through day"),
    },
)
st.caption(
    f"{FULL_LABEL} is blank until the panel reaches day +{END} after the filing date. "
    "'CAR to date' is cumulative abnormal return through the day in 'CAR through day'."
)

# ---- Summary by trade type ---------------------------------------------------
st.subheader("Average CAR by trade type")
measure = st.radio(
    "Measure",
    [FULL_LABEL, "CAR to date (mixed horizons)"],
    index=0 if view[CAR_FULL].notna().any() else 1,
    horizontal=True,
    help="CAR to date averages events observed over different numbers of days; "
         "use it only for a quick look.",
)
col = CAR_FULL if measure == FULL_LABEL else "car_to_date"
summary = (view.dropna(subset=[col]).groupby("trade_type")[col]
           .agg(n="count", mean_car="mean").reindex(config.TRADE_TYPES).dropna(how="all"))

if summary.empty:
    st.info("No events with return data for this measure in the current selection.")
else:
    st.dataframe(
        summary.reset_index(), hide_index=True,
        column_config={"mean_car": st.column_config.NumberColumn("mean CAR", format="percent"),
                       "n": st.column_config.NumberColumn("events")},
    )
st.caption(f"Source: {TX_PATH.relative_to(config.ROOT).as_posix()} joined to "
           f"{PANEL_PATH.relative_to(config.ROOT).as_posix()} on accession.")
