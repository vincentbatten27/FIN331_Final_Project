"""Intro page. Owner: Product manager (David).

The question, who would pay for the answer, and a short summary of the finding.
The headline numbers and the summary sentence are built from
outputs/summary_by_trade_type.csv (or outputs/sample/ with a SAMPLE DATA warning).
Rules: read only from outputs/ or data/sample/; no downloads or model fitting here;
no hard-coded numbers.
"""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import config  # noqa: E402

st.set_page_config(page_title="Intro", layout="wide")
st.title("Do insider purchases predict returns?")

roles = " and ".join(config.ROLES)
roles_plural = " and ".join(f"{r}s" for r in config.ROLES)


def events(n) -> str:
    n = int(n)
    return f"{n} event" if n == 1 else f"{n} events"


st.subheader("The question")
st.markdown(
    f"When a company's {roles} buy their own stock on the open market, they file a "
    "Form 4 with the SEC. Does the stock earn abnormal returns after that filing becomes "
    "public? And are some insiders more informative than others?\n\n"
    "Cohen, Malloy & Pomorski (2012) split insiders into **routine** traders, who trade "
    "in the same calendar month year after year, and **opportunistic** traders, who do "
    "not. Their finding: the routine trades carry little information, while the "
    "opportunistic ones predict returns. We test that idea on recent filings by "
    f"{roles_plural} of S&P 500 firms."
)

st.subheader("Who would pay")
st.markdown(
    "A **stock screener**. Insider filings are free and public, but they are noisy: most "
    "trades are routine, planned (10b5-1) or small. A screener that flags today's "
    "*opportunistic* purchases, and shows how similar trades have done historically, "
    "turns that noise into a short list worth a look."
)

# ---- Headline (built from the summary file) ------------------------------------
st.subheader("What we find")
real = config.OUTPUTS / "summary_by_trade_type.csv"
sample = config.OUTPUTS / "sample" / "summary_by_trade_type.csv"
path = real if real.exists() else sample if sample.exists() else None

if path is None:
    st.info("No results yet: summary_by_trade_type.csv is not in outputs/.")
else:
    if path == sample:
        st.warning("SAMPLE DATA: the numbers below come from fake rows in outputs/sample/. "
                   "Not real results.")
    s = pd.read_csv(path).set_index("trade_type")
    day = int(s["t_used"].max())
    shown = [t for t in ["opportunistic", "routine"] if t in s.index]

    cols = st.columns(len(shown) + 1)
    for col, t in zip(cols, shown):
        col.metric(f"Mean CAR, {t}", f"{s.loc[t, 'mean_car']:.2%}",
                   help=f"Average cumulative abnormal return through day +{day} after the "
                        f"filing date, over {int(s.loc[t, 'n'])} events.")
    cols[-1].metric("Events with returns", f"{int(s['n'].drop('all', errors='ignore').sum())}")

    if len(shown) == 2:
        o, r = s.loc["opportunistic"], s.loc["routine"]
        gap = o["mean_car"] - r["mean_car"]
        word = "higher" if gap > 0 else "lower" if gap < 0 else "the same as"
        gap_txt = (f"{abs(gap) * 100:.2f} percentage points {word} than" if gap != 0
                   else word)
        st.markdown(
            f"Through day +{day} after the filing date, opportunistic purchases averaged a "
            f"CAR of {o['mean_car']:.2%} ({events(o['n'])}), {gap_txt} routine purchases "
            f"at {r['mean_car']:.2%} ({events(r['n'])}). "
            "See **Results** for standard errors and the chart, and **Methodology** for how "
            "these are measured."
        )
    st.caption(f"Source: {path.relative_to(config.ROOT).as_posix()}")
