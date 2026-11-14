# Specifications tried

Log every spec you run, including ones that did not work. One row each, newest last.
Never delete rows.

| Date | Who | Spec (filters, window, benchmark, classification) | Command / script | Output file | Result in one line | Kept? |
|---|---|---|---|---|---|---|
| 2026-11-14 | Eric | v0 universe: 10 tickers drawn with seed 331 from the Jan-1-2021 S&P 500 list (sorted, then `DataFrame.sample`) | `src/sp500_membership.py` | `data/output/v0_universe.csv` | BWA, EOG, LKQ, NOC, NVR, PEG, PPG, UPS, WST, WY | yes |
| 2026-11-14 | Eric | Purchases: Form 4 code P, acquired (A); role from owner title (CEO / Chief Executive Officer, CFO / Chief Financial Officer; division "CEO-..." titles excluded; CEO wins ties); firms matched by issuer CIK; filings 2018-01-01 to 2021-06-30; same purchase in several filings or 4/A kept once (earliest filing); one row per accession (usd_value summed, earliest trans_date); is_10b5_1 from a 10b5-1 mention in the purchase's footnotes or filing remarks (AFF10B5ONE only exists in 2023+ data sets) | `src/build_transactions.py` | `data/output/transactions.csv` | 7 purchases: 1 in the event window (WY CFO, filed 2021-05-06), 6 history rows; 0 flagged 10b5-1 (detector flags 2 of 6 CEO/CFO sales in 2021H1, so it works) | yes |
| 2026-11-14 | Eric | Market model on SPY, estimation (-250,-30) trading days, min 120 valid days, event window (+1,+20); day 0 = first trading day on/after the filing date; size >= $10,000; 10b5-1 excluded | `src/event_study.py` | `data/output/event_panel.csv` | 1 event; WY CAR[+1,+20] = -0.1065 (alpha 0.00076, beta 1.551, 221 estimation days); hand recompute matches | yes |
