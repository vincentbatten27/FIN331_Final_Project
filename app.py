"""Landing page and navigation. Owner: Product manager (David).

Home is the screener view: the latest opportunistic purchases, each with the
historical CAR of similar trades (same role, also opportunistic) whose return window
had already closed before that purchase was filed, so nothing shown uses later
information. Links to the four pages. Reads data/output/ when both contract files
exist, otherwise data/sample/ with a SAMPLE DATA warning.
Rules: read only from data/output/, outputs/ or data/sample/; no downloads or model
fitting here; no hard-coded numbers (window, roles, filters come from src/config.py).
"""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
import config  # noqa: E402

START, END = config.EVENT_WINDOW
LATEST_N = 10  # rows shown in the screener table (display setting, not a study parameter)

PAGES = [
    ("pages/1_Intro.py", "Intro", "The question, who would pay, and the headline.",
     ":material/info:"),
    ("pages/2_Methodology.py", "Methodology", "Data, parameters, pipeline, threats.",
     ":material/schema:"),
    ("pages/3_Results.py", "Results", "CAR by trade type, chart and sample description.",
     ":material/bar_chart:"),
    ("pages/4_Explore.py", "Explore", "Filter every purchase and its CAR.",
     ":material/table:"),
]


@st.cache_data
def load(tx_path: str, panel_path: str) -> pd.DataFrame:
    """One row per purchase with its CAR, the day it runs through, and the date that day ends."""
    tx = pd.read_csv(tx_path, parse_dates=["filing_date", "trans_date"])
    panel = pd.read_csv(panel_path, parse_dates=["filing_date", "date"])
    panel = panel[panel["t"].between(START, END)]
    last = (panel.sort_values("t").groupby("accession").tail(1)[["accession", "t", "date", "CAR"]]
            .rename(columns={"t": "car_day", "date": "car_end_date"}))
    return tx.merge(last, on="accession", how="left")


def similar_car(row: pd.Series, past: pd.DataFrame, full_only: bool) -> pd.Series:
    """Mean CAR of earlier opportunistic trades by the same role, known by row's filing date."""
    m = past[(past["role"] == row["role"])
             & (past["car_end_date"] < row["filing_date"])
             & (past["accession"] != row["accession"])]
    if full_only:
        m = m[m["car_day"] == END]
    return pd.Series({"similar_n": len(m),
                      "similar_mean_car": m["CAR"].mean() if len(m) else float("nan")})


def home() -> None:
    using_sample = not (config.TRANSACTIONS_CSV.exists() and config.EVENT_PANEL_CSV.exists())
    tx_path = config.SAMPLE_TRANSACTIONS_CSV if using_sample else config.TRANSACTIONS_CSV
    panel_path = config.SAMPLE_EVENT_PANEL_CSV if using_sample else config.EVENT_PANEL_CSV
    roles = " and ".join(f"{r}s" for r in config.ROLES)

    st.title("Do insider purchases predict returns?")
    st.markdown(
        f"A screener for open-market purchases by {roles} of S&P 500 firms. It flags "
        "**opportunistic** buys, which break the insider's usual calendar pattern, and "
        "shows how similar trades did after their filing date."
    )
    if using_sample:
        st.warning("SAMPLE DATA: fake rows from data/sample/. Not real results. "
                   "Real purchases appear once the pipeline writes data/output/.")

    df = load(str(tx_path), str(panel_path))
    if config.EXCLUDE_10B5_1:
        df = df[df["is_10b5_1"] == 0]
    opp = df[df["trade_type"] == "opportunistic"]
    past = opp.dropna(subset=["CAR"])

    # Prefer full-window CARs; fall back to CAR to date only if no event has a full window.
    full_only = bool((past["car_day"] == END).any())
    car_label = f"CAR[+{START},+{END}]" if full_only else "CAR to date"

    st.subheader("Latest opportunistic purchases")
    latest = opp.sort_values("filing_date", ascending=False).head(LATEST_N)
    if latest.empty:
        st.info("No opportunistic purchases in the data.")
    else:
        latest = pd.concat([latest, latest.apply(similar_car, axis=1, past=past,
                                                 full_only=full_only)], axis=1)
        st.dataframe(
            latest[["filing_date", "ticker", "role", "usd_value", "similar_n",
                    "similar_mean_car"]],
            hide_index=True,
            width="stretch",
            column_config={
                "filing_date": st.column_config.DateColumn("filed", format="YYYY-MM-DD"),
                "usd_value": st.column_config.NumberColumn("$ size", format="$%,.0f"),
                "similar_n": st.column_config.NumberColumn("similar past trades"),
                "similar_mean_car": st.column_config.NumberColumn(
                    f"their mean {car_label}", format="percent"),
            },
        )
        st.caption(
            f"Most recent filings in {tx_path.relative_to(config.ROOT).as_posix()}"
            + (" (10b5-1 planned trades excluded)" if config.EXCLUDE_10B5_1 else "")
            + ". 'Similar' = earlier opportunistic purchases by the same role whose return "
            "window had closed before this filing date."
            + ("" if full_only else f" No event in this data reaches day +{END} yet, so "
                                    "this uses CAR to the last available day.")
        )

    st.subheader("Go to")
    for col, (page, label, blurb, icon) in zip(st.columns(len(PAGES)), PAGES):
        with col.container(border=True):
            st.page_link(page, label=label, icon=icon)
            st.caption(blurb)


st.set_page_config(page_title="Insider purchases", layout="wide")
nav = st.navigation(
    [st.Page(home, title="Home", icon=":material/home:", default=True)]
    + [st.Page(page, title=label, icon=icon) for page, label, _, icon in PAGES]
)
nav.run()
