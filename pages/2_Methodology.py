"""Methodology page. Owner: Product manager (David).

Data sources, the pipeline steps (match the README table), the routine rule, the
event window and the threats to validity. Every parameter is read from
src/config.py; none is retyped here.
Rules: read only from outputs/ or data/sample/; no downloads or model fitting here;
no hard-coded numbers.
"""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import config  # noqa: E402

st.set_page_config(page_title="Methodology", layout="wide")
st.title("Methodology")

ev0, ev1 = config.EVENT_WINDOW
es0, es1 = config.ESTIMATION_WINDOW
roles = ", ".join(config.ROLES)

st.info(
    "**The event date is the filing date**, the day the Form 4 becomes public, never the "
    f"trade date. Abnormal returns are measured from day +{ev0} to day +{ev1} after it."
)

# ---- Data ----------------------------------------------------------------------
st.subheader("Data (all free)")
st.markdown(
    "- **SEC insider transactions data sets** (quarterly zips of Forms 3, 4 and 5): "
    "who bought, when it was filed, when it traded, size, and the 10b5-1 flag.\n"
    "- **Stock and market prices** from yfinance, for returns and the market benchmark.\n"
    "- **S&P 500 membership**: yearly January 1 constituent lists, updated with the "
    "Wikipedia S&P 500 changes table for additions and removals during the year.\n"
    "- **Ken French factors**, for robustness checks if used."
)
st.caption("Where each file came from and when it was pulled is logged in DATA_SOURCES.md.")

# ---- Sample and parameters -----------------------------------------------------
st.subheader("Sample and parameters")
params = pd.DataFrame(
    [
        ("Filing dates", f"{config.SAMPLE_START:%Y-%m-%d} to {config.SAMPLE_END:%Y-%m-%d}"),
        ("Insiders", roles),
        ("Transaction", f"Form 4 code {config.TRANSACTION_CODE} (open-market purchase)"),
        ("Firms", "S&P 500 members as of the filing date (point in time)"),
        ("Minimum trade size", f"${config.MIN_USD_VALUE:,.0f}"),
        ("10b5-1 planned trades", "excluded from the main spec" if config.EXCLUDE_10B5_1
         else "included in the main spec"),
        ("Event window", f"[+{ev0}, +{ev1}] trading days after the filing date"),
        ("Estimation window", f"[{es0}, {es1}] trading days, at least "
                              f"{config.MIN_ESTIMATION_DAYS} valid returns"),
        ("Benchmark", f"market model on {config.MARKET_PROXY}"),
        ("Routine rule", f"traded in the same calendar month in each of the prior "
                         f"{config.ROUTINE_LOOKBACK_YEARS} years"),
        ("History for the routine rule", f"from {config.HISTORY_START:%Y-%m-%d}"),
    ],
    columns=["Choice", "Value"],
)
st.dataframe(params, hide_index=True, width="stretch")
st.caption("Read live from src/config.py. Some values are still proposed and awaiting team "
           "sign-off (see README, Choices).")

# ---- Routine vs opportunistic ---------------------------------------------------
st.subheader("Routine vs opportunistic")
st.markdown(
    f"Following Cohen, Malloy & Pomorski (2012), an insider is **routine** if they traded "
    f"in the same calendar month in each of the {config.ROUTINE_LOOKBACK_YEARS} years before "
    "the trade, and **opportunistic** if they have enough history but no such pattern. "
    "Insiders without enough history are **unclassified**. Only trades *before* each "
    "purchase are used, so the label never peeks at the future."
)

# ---- Pipeline --------------------------------------------------------------------
st.subheader("Pipeline")
steps = pd.DataFrame(
    [
        ("1", "Download SEC insider data sets", "src/fetch_sec.py", "data/raw/"),
        ("2", "Build purchase table (dedupe on accession, filing date, 10b5-1 flag)",
         "src/build_transactions.py", "data/output/transactions.csv"),
        ("3", "Point-in-time S&P 500 membership", "src/sp500_membership.py",
         "data/output/sp500_membership.csv"),
        ("4", "Prices, market proxy, factors", "src/fetch_prices.py", "data/raw/"),
        ("5", "Event study (market model, AR, CAR)", "src/event_study.py",
         "data/output/event_panel.csv"),
        ("6", "Routine / opportunistic classification", "src/classify_insiders.py",
         "trade_type in transactions.csv"),
        ("7", "Tables and figures", "src/report.py", "outputs/"),
        ("8", "Dashboard (this site)", "app.py, pages/", "reads outputs/"),
    ],
    columns=["Step", "What", "Script", "Output"],
)
st.dataframe(steps, hide_index=True, width="stretch")
st.markdown(
    f"**Abnormal return.** For each event, a market model (stock return on "
    f"{config.MARKET_PROXY} return) is estimated over days {es0} to {es1}. The abnormal "
    "return each day is the actual return minus the model's expected return. CAR adds up "
    f"the abnormal returns from day +{ev0} to day +{ev1}."
)

# ---- Threats -----------------------------------------------------------------------
st.subheader("Threats to validity")
st.markdown(
    "- **Transaction date vs filing date:** insiders can file days after trading. We date "
    "every event at the filing date, when the market can first see it.\n"
    "- **10b5-1 plans:** planned trades carry no new information. They are flagged by "
    "`is_10b5_1`, and the flag is only reliable in recent filings.\n"
    "- **Duplicate filings and amendments:** removed once, keyed on the accession number.\n"
    "- **Look-ahead:** the routine label uses only earlier trades, and S&P 500 membership "
    "is as of the filing date.\n"
    "- **S&P 500 membership:** rebuilt from free lists, not a vendor point-in-time file, so "
    "mid-year changes and reused tickers can be misdated.\n"
    "- **Survivorship:** firms delisted or acquired may be missing from free price data, "
    "which can bias returns upward.\n"
    f"- **Overlapping events:** repeat purchases within {ev1} trading days share return "
    "windows, so observations are not independent and t-stats are descriptive."
)
