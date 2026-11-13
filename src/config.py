"""Single source of truth for paths and study parameters.

Ask the team before changing anything here (see CLAUDE.md). Values marked
"proposed" are defaults awaiting team sign-off.
"""
import os
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

# ---- Paths -----------------------------------------------------------------
DATA_RAW = ROOT / "data" / "raw"        # downloads, git-ignored
DATA_TEMP = ROOT / "data" / "temp"      # scratch / caches, git-ignored
DATA_OUTPUT = ROOT / "data" / "output"  # contract files passed between steps
DATA_SAMPLE = ROOT / "data" / "sample"  # fake rows, used by the app and tests
OUTPUTS = ROOT / "outputs"              # every number/figure shown to users
AUDITS = ROOT / "audits"

TRANSACTIONS_CSV = DATA_OUTPUT / "transactions.csv"
EVENT_PANEL_CSV = DATA_OUTPUT / "event_panel.csv"
SAMPLE_TRANSACTIONS_CSV = DATA_SAMPLE / "transactions.csv"
SAMPLE_EVENT_PANEL_CSV = DATA_SAMPLE / "event_panel.csv"
# Yearly S&P 500 constituents as of Jan 1 (one row per year, first column = year).
SP500_YEARLY_CSV = ROOT / "data" / "reference" / "spx_yearly_tickers.csv"  # committed

# ---- Sample period (by FILING date) -- proposed ------------------------------
# 3-year MVP window. History before SAMPLE_START feeds the routine classifier.
SAMPLE_START = date(2020, 1, 1)
SAMPLE_END = date(2022, 12, 31)
HISTORY_START = date(2017, 1, 1)   # 3 prior years for the routine rule

# ---- Checkpoint 2 (v0) scope -- proposed --------------------------------------------
# Small end-to-end run. Draw V0_N_FIRMS tickers with SEED from the S&P 500 list
# as of Jan 1 of V0_EVENT_START's year; never pick tickers by hand or from memory.
V0_N_FIRMS = 10
V0_EVENT_START = date(2021, 1, 1)   # filing dates
V0_EVENT_END = date(2021, 6, 30)
V0_HISTORY_START = date(2018, 1, 1)  # 3 prior years for the routine rule

# ---- Event study ---------------------------------------------------------------
EVENT_WINDOW = (1, 20)          # CAR[+1,+20] in trading days from the filing date
ESTIMATION_WINDOW = (-250, -30)  # market-model estimation window
MIN_ESTIMATION_DAYS = 120       # proposed; drop events with fewer valid returns
MARKET_PROXY = "SPY"            # proposed benchmark (yfinance)

# ---- Sample filters -- proposed ------------------------------------------------
ROLES = ["CEO", "CFO"]
MIN_USD_VALUE = 10_000          # proposed size filter
EXCLUDE_10B5_1 = True           # proposed: drop 10b5-1 trades from the main spec
TRANSACTION_CODE = "P"          # Form 4 code P = open-market purchase
TRADE_TYPES = ["routine", "opportunistic", "unclassified"]  # trade_type values

# ---- Routine vs opportunistic (Cohen, Malloy & Pomorski 2012) -- proposed --------
# Routine = traded in the same calendar month in each of the prior N years.
ROUTINE_LOOKBACK_YEARS = 3

# ---- Reproducibility -------------------------------------------------------------
SEED = 331


# ---- SEC access ----------------------------------------------------------------
def sec_user_agent() -> str:
    """User-Agent for SEC requests, read from .env. Fails loudly if blank."""
    ua = os.getenv("SEC_USER_AGENT", "").strip()
    if not ua:
        raise RuntimeError(
            "SEC_USER_AGENT is empty. Copy .env.example to .env and set it "
            "to 'Your Name your.email@lehigh.edu'."
        )
    return ua
