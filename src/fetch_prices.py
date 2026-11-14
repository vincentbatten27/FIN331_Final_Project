"""Step 4: download prices and the market proxy.

Owner: Developer (Eric).

Output : daily adjusted prices for the v0_universe tickers and config.MARKET_PROXY
         in data/raw/prices/<ticker>.csv (date, close), then data/raw/prices_done.flag.
Window : from about 400 calendar days before config.V0_EVENT_START (to cover
         config.ESTIMATION_WINDOW) to 40 days after config.V0_EVENT_END.
         Both buffers are derived from the config windows (CAL_PER_TRADING_DAY).
Rules  : yfinance only; skip files already downloaded; record the date pulled in
         DATA_SOURCES.md; report tickers with missing prices instead of dropping
         them silently.

Rules: event date is the filing date; never fill data from memory (look up
file layouts in the official documentation); no hard-coded numbers (use
src/config.py); keep the contract columns in README.md exactly; log any spec you
try in specs_tried.md.
"""
import sys
from datetime import date, timedelta

import pandas as pd
import yfinance as yf

import config
import sp500_membership

PRICES_DIR = config.DATA_RAW / "prices"
FLAG = config.DATA_RAW / "prices_done.flag"
CAL_PER_TRADING_DAY = 1.6  # generous calendar-days-per-trading-day, so windows are covered


def window() -> tuple[date, date]:
    start = config.V0_EVENT_START - timedelta(days=round(-config.ESTIMATION_WINDOW[0] * CAL_PER_TRADING_DAY))
    end = config.V0_EVENT_END + timedelta(days=round(config.EVENT_WINDOW[1] * 2))
    return start, end


def yahoo_symbol(ticker: str) -> str:
    """Share-class tickers use '-' on Yahoo (BRK.B, BF/B -> BRK-B, BF-B)."""
    return ticker.replace(".", "-").replace("/", "-")


def price_path(ticker: str):
    return PRICES_DIR / f"{ticker.replace('/', '-')}.csv"


def fetch(ticker: str, start: date, end: date) -> pd.DataFrame:
    raw = yf.download(yahoo_symbol(ticker), start=start, end=end, auto_adjust=True,
                      progress=False, multi_level_index=False)
    if raw.empty or "Close" not in raw:
        return pd.DataFrame(columns=["date", "close"])
    out = raw[["Close"]].dropna().reset_index()
    out.columns = ["date", "close"]
    out["date"] = pd.to_datetime(out["date"]).dt.date
    return out


def main() -> None:
    PRICES_DIR.mkdir(parents=True, exist_ok=True)
    start, end = window()
    tickers = list(pd.read_csv(sp500_membership.UNIVERSE_CSV)["ticker"]) + [config.MARKET_PROXY]
    missing = []
    for t in tickers:
        path = price_path(t)
        if path.exists() and len(pd.read_csv(path)):
            print(f"{t}: already downloaded")
            continue
        df = fetch(t, start, end)
        if df.empty:
            missing.append(t)
            print(f"{t}: NO PRICES from yfinance")
            continue
        df.to_csv(path, index=False)
        print(f"{t}: {len(df)} days, {df['date'].min()} to {df['date'].max()}")

    if config.MARKET_PROXY in missing:
        sys.exit(f"No prices for the market proxy {config.MARKET_PROXY}; cannot run the event study.")
    note = f"MISSING: {', '.join(missing)}" if missing else "missing: none"
    FLAG.write_text(f"pulled {date.today()} from yfinance, window {start} to {end}\n{note}\n")
    print(f"window {start} to {end}; {note}")


if __name__ == "__main__":
    main()
