"""Results page. Owner: Product manager (David).

Shows outputs/summary_by_trade_type.csv, outputs/car_by_trade_type.png and
outputs/data_description.csv (written by src/report.py and src/data_description.py).
Each file falls back to outputs/sample/ with a visible SAMPLE DATA warning when the
real one does not exist yet.
Rules: read only from outputs/ or data/sample/; no downloads or model fitting here;
no hard-coded numbers.
"""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import config  # noqa: E402

st.set_page_config(page_title="Results", layout="wide")
st.title("Results")

SAMPLE_DIR = config.OUTPUTS / "sample"
FILES = ["summary_by_trade_type.csv", "car_by_trade_type.png", "data_description.csv"]


def resolve(name: str) -> tuple[Path | None, bool]:
    """Return (path, is_sample). Real file in outputs/ wins; else outputs/sample/."""
    real, sample = config.OUTPUTS / name, SAMPLE_DIR / name
    if real.exists():
        return real, False
    if sample.exists():
        return sample, True
    return None, False


def rel(p: Path) -> str:
    return p.relative_to(config.ROOT).as_posix()


paths = {name: resolve(name) for name in FILES}
sample_files = [n for n, (p, s) in paths.items() if s]
if sample_files:
    st.warning(
        "SAMPLE DATA: fake results from outputs/sample/ for "
        + ", ".join(sample_files)
        + ". Not real results. Real files appear once src/report.py writes outputs/."
    )

START, END = config.EVENT_WINDOW

# ---- Summary table -----------------------------------------------------------
st.subheader("Cumulative abnormal return after the filing date, by trade type")
path, _ = paths["summary_by_trade_type.csv"]
if path is None:
    st.error("summary_by_trade_type.csv not found in outputs/ or outputs/sample/.")
else:
    summary = pd.read_csv(path)
    t_used = int(summary["t_used"].max())
    if t_used < END:
        st.info(
            f"These CARs run through day +{t_used}, not the full window "
            f"[+{START},+{END}] set in src/config.py."
        )
    st.dataframe(
        summary,
        hide_index=True,
        column_config={
            "trade_type": "trade type",
            "n": st.column_config.NumberColumn("events"),
            "mean_car": st.column_config.NumberColumn("mean CAR", format="percent"),
            "std_car": st.column_config.NumberColumn("std. dev. CAR", format="percent"),
            "t_stat": st.column_config.NumberColumn("t-stat", format="%.2f"),
            "t_used": st.column_config.NumberColumn("CAR through day"),
        },
    )
    st.caption(
        "Events that overlap in time are not independent, so t-stats are descriptive. "
        f"Source: {rel(path)}"
    )

# ---- Figure ------------------------------------------------------------------
path, _ = paths["car_by_trade_type.png"]
if path is None:
    st.error("car_by_trade_type.png not found in outputs/ or outputs/sample/.")
else:
    left, _ = st.columns([3, 2])
    left.image(str(path), caption=f"Mean CAR with 95% confidence intervals. Source: {rel(path)}",
               width="stretch")

# ---- Data description --------------------------------------------------------
st.subheader("The sample")
path, _ = paths["data_description.csv"]
if path is None:
    st.error("data_description.csv not found in outputs/ or outputs/sample/.")
else:
    desc = pd.read_csv(path)
    st.dataframe(desc, hide_index=True)
    st.caption(f"Source: {rel(path)}")
