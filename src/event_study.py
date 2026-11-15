"""Step 5: market-model event study (data/output/event_panel.csv).

Owner: Developer (Eric).

Inputs : transactions.csv, prices in data/raw/.
Output : config.EVENT_PANEL_CSV with exactly the columns in README.md.
Do     : events = rows with filing_date in config.V0_EVENT_START..V0_EVENT_END,
         excluding 10b5-1 trades if config.EXCLUDE_10B5_1 and trades under
         config.MIN_USD_VALUE. Day 0 is the filing date; t counts trading days.
         Estimate the market model over config.ESTIMATION_WINDOW, require
         config.MIN_ESTIMATION_DAYS valid returns, then compute ret, mkt, expected,
         AR and cumulative CAR for t in config.EVENT_WINDOW.
Checks : assert (accession, t) is unique; hand-recompute one event and match;
         run contracts.validate_event_panel on the output.

Trading days are the market proxy's trading days. If a filing date is not a
trading day, day 0 is the next trading day (the first day the market could react).
Events without a full event window or enough estimation days are dropped and
listed, never filled.

Rules: event date is the filing date; never fill data from memory (look up
file layouts in the official documentation); no hard-coded numbers (use
src/config.py); keep the contract columns in README.md exactly; log any spec you
try in specs_tried.md.
"""
import numpy as np
import pandas as pd

import config
import contracts
from fetch_prices import price_path

TOLERANCE = 1e-10  # agreement required between the pipeline and the hand recompute


def returns(ticker: str) -> pd.Series:
    px = pd.read_csv(price_path(ticker), parse_dates=["date"]).set_index("date")["close"]
    return px.pct_change()


def select_events(tx: pd.DataFrame) -> pd.DataFrame:
    ev = tx[tx["filing_date"].between(pd.Timestamp(config.V0_EVENT_START), pd.Timestamp(config.V0_EVENT_END))]
    ev = ev[ev["usd_value"] >= config.MIN_USD_VALUE]
    if config.EXCLUDE_10B5_1:
        ev = ev[ev["is_10b5_1"] == 0]
    return ev


def event_rows(event, ret: pd.Series, mkt: pd.Series):
    """Panel rows for one event, or (None, reason) if it cannot be estimated."""
    days = mkt.index
    i0 = days.searchsorted(event.filing_date)  # first trading day on/after the filing date
    lo, hi = i0 + config.ESTIMATION_WINDOW[0], i0 + config.ESTIMATION_WINDOW[1]
    e_lo, e_hi = i0 + config.EVENT_WINDOW[0], i0 + config.EVENT_WINDOW[1]
    if lo < 1 or e_hi >= len(days):
        return None, "price history does not cover the estimation and event windows"

    est = pd.DataFrame({"ret": ret.reindex(days[lo:hi + 1]), "mkt": mkt.iloc[lo:hi + 1]}).dropna()
    if len(est) < config.MIN_ESTIMATION_DAYS:
        return None, f"only {len(est)} valid estimation days (< {config.MIN_ESTIMATION_DAYS})"
    beta = est["ret"].cov(est["mkt"]) / est["mkt"].var()
    alpha = est["ret"].mean() - beta * est["mkt"].mean()

    win = pd.DataFrame({"date": days[e_lo:e_hi + 1],
                        "t": range(config.EVENT_WINDOW[0], config.EVENT_WINDOW[1] + 1)})
    win["ret"] = ret.reindex(win["date"]).values
    win["mkt"] = mkt.iloc[e_lo:e_hi + 1].values
    if win[["ret", "mkt"]].isna().any().any():
        return None, "missing returns inside the event window"
    win["expected"] = alpha + beta * win["mkt"]
    win["AR"] = win["ret"] - win["expected"]
    win["CAR"] = win["AR"].cumsum()
    win["accession"], win["ticker"], win["filing_date"] = event.accession, event.ticker, event.filing_date
    return win, None


def hand_check(panel: pd.DataFrame, rets: dict, mkt: pd.Series) -> None:
    """Recompute one randomly chosen event's CAR[last t] with an independent method
    (np.polyfit on calendar-indexed data) and require it to match the panel."""
    acc = panel["accession"].drop_duplicates().sample(1, random_state=config.SEED).iloc[0]
    ev = panel[panel["accession"] == acc]
    ticker, filed = ev["ticker"].iloc[0], ev["filing_date"].iloc[0]
    both = pd.concat({"r": rets[ticker], "m": mkt}, axis=1, join="inner")
    both = both[both["m"].notna()]
    day0 = both.index[both.index >= filed][0]
    pos = both.index.get_loc(day0)
    est = both.iloc[pos + config.ESTIMATION_WINDOW[0]: pos + config.ESTIMATION_WINDOW[1] + 1].dropna()
    slope, intercept = np.polyfit(est["m"], est["r"], 1)
    evw = both.iloc[pos + config.EVENT_WINDOW[0]: pos + config.EVENT_WINDOW[1] + 1]
    car = float((evw["r"] - (intercept + slope * evw["m"])).sum())
    panel_car = float(ev.loc[ev["t"] == config.EVENT_WINDOW[1], "CAR"].iloc[0])
    print(f"hand check {acc} ({ticker}, filed {filed.date()}): recomputed CAR = {car:.6f}, "
          f"panel CAR = {panel_car:.6f}")
    assert abs(car - panel_car) < TOLERANCE, "hand-recomputed CAR does not match the panel"


def main() -> None:
    tx = pd.read_csv(config.TRANSACTIONS_CSV, parse_dates=["filing_date", "trans_date"])
    events = select_events(tx)
    mkt = returns(config.MARKET_PROXY)
    rets = {t: returns(t) for t in events["ticker"].unique() if price_path(t).exists()}

    pieces, dropped = [], []
    for ev in events.itertuples():
        if ev.ticker not in rets:
            dropped.append((ev.accession, ev.ticker, "no price file"))
            continue
        rows, why = event_rows(ev, rets[ev.ticker], mkt)
        if rows is None:
            dropped.append((ev.accession, ev.ticker, why))
        else:
            pieces.append(rows)

    panel = (pd.concat(pieces, ignore_index=True) if pieces
             else pd.DataFrame(columns=contracts.EVENT_PANEL_COLUMNS))[contracts.EVENT_PANEL_COLUMNS]
    assert not panel.duplicated(["accession", "t"]).any(), "(accession, t) is not unique"
    if len(panel):
        hand_check(panel, rets, mkt)

    out = panel.copy()
    out["filing_date"] = pd.to_datetime(out["filing_date"]).dt.date
    out["date"] = pd.to_datetime(out["date"]).dt.date
    config.DATA_OUTPUT.mkdir(parents=True, exist_ok=True)
    out.to_csv(config.EVENT_PANEL_CSV, index=False)
    problems = contracts.validate_event_panel(config.EVENT_PANEL_CSV)
    if problems:
        raise SystemExit("contract problems:\n  " + "\n  ".join(problems))

    print(f"event_panel.csv: {panel['accession'].nunique()} events x {len(panel['t'].unique())} days "
          f"({len(events)} eligible purchases, {len(dropped)} dropped)")
    for acc, t, why in dropped:
        print(f"  dropped {acc} ({t}): {why}")
    if len(panel):
        last = panel[panel["t"] == config.EVENT_WINDOW[1]][["accession", "ticker", "filing_date", "CAR"]]
        print(last.to_string(index=False))


if __name__ == "__main__":
    main()
