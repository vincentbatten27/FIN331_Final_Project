"""Minimal dashboard. Reads data/sample/ only (fake rows) until real outputs exist."""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
import config  # noqa: E402

st.set_page_config(page_title="Insider purchases", layout="wide")
st.title("Do insider purchases predict returns?")
st.warning("SAMPLE DATA: fake rows from data/sample/. Not real results.")


@st.cache_data
def load():
    tx = pd.read_csv(config.SAMPLE_TRANSACTIONS_CSV, parse_dates=["filing_date", "trans_date"])
    panel = pd.read_csv(config.SAMPLE_EVENT_PANEL_CSV, parse_dates=["filing_date", "date"])
    return tx, panel


tx, panel = load()

types = st.multiselect("Trade type", config.TRADE_TYPES, default=config.TRADE_TYPES)
include_10b5_1 = st.checkbox("Include 10b5-1 trades", value=not config.EXCLUDE_10B5_1)

view = tx[tx["trade_type"].isin(types)]
if not include_10b5_1:
    view = view[view["is_10b5_1"] == 0]

# CAR at the last available day of each event, computed from the panel.
last = panel.sort_values("t").groupby("accession").tail(1)[["accession", "t", "CAR"]]
view = view.merge(last, on="accession", how="left")

st.subheader("Purchases")
st.dataframe(view, width="stretch")

st.subheader("Average CAR at last available day, by trade type")
summary = view.dropna(subset=["CAR"]).groupby("trade_type")["CAR"].agg(["count", "mean"])
if summary.empty:
    st.info("No events with return data in the current selection.")
else:
    st.dataframe(summary)
