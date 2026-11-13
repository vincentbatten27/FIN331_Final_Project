# Context for the agent
Here is the summary of the project:  Question 8. Do insider purchases predict returns? Are "opportunistic" insiders more informative than "routine" ones (Cohen, Malloy & Pomorski, 2012)? Who'd pay: a stock screener product. Row: insider purchase (filing date, insider role, $ size, routine or opportunistic, CAR[+1,+20]). Data: the SEC's structured Form 3/4/5 data sets (quarterly zips, free), and returns. Method: an event study from the filing date (the day it's public), and a classification of routine traders by their past timing. Dashboard: today's opportunistic purchases, with the historical CAR for similar trades. MVP: purchases by CEOs and CFOs of S&P 500 firms, 3 years. Stretch: sales are mostly noise. Show it. Auditors will poke at: transaction date vs. filing date (use the filing date), 10b5-1 planned trades, and duplicate filings.

Here is a target row set up: One row per insider open-market purchase:
accession	issuer_cik	ticker	insider_cik	role	filing_date	trans_date	usd_value	is_10b5_1	trade_type	car_1_20

Hard rules:
The event date is the filing date. Never use the trade date as the event date.
Use only information available before each trade, so there’s no look-ahead.
Use point-in-time S&P 500 membership.
Never hard-code results. Everything shown must be produced by code into outputs/.
Never fetch or fill data from model memory.
Log every spec in specs_tried.md.

## Project decisions (see README "Choices"; "proposed" = awaiting team sign-off)

- Free sources only: SEC insider transactions data sets, yfinance, Ken French factors, Wikipedia S&P 500 changes, plus the yearly Jan-1 S&P 500 ticker list. No WRDS, no paid data, no LLM/API keys.
- Sample: filing dates 2020-01-01 to 2022-12-31 (proposed), CEO and CFO purchases only (code P) of S&P 500 members.
- Event window (+1,+20); estimation window (-250,-30); market model on SPY (proposed); size filter $10,000 (proposed); 10b5-1 flagged and excluded from the main spec (proposed); routine = same calendar month in each of the prior 3 years (proposed).
- `trade_type` in `transactions.csv` is `routine`, `opportunistic` or `unclassified`.
- Contract files between steps: `data/output/transactions.csv` and `data/output/event_panel.csv` (schemas in README). `data/sample/` holds fake rows for the app.

## Hard rules (all agents and teammates)

1. Event date = filing date. Never use the trade date as the event date.
2. No look-ahead: use only information available before each trade or event (classification history, S&P membership, estimation window).
3. Use point-in-time S&P 500 membership as of the event date.
4. No hard-coded numbers. Every number, table and figure shown must be produced by code into `outputs/`. Parameters live in `src/config.py`.
5. Never fetch or fill data from model memory. If a source is unavailable, stop and say so.
6. Log every specification you run in `specs_tried.md`, including failures.
7. Stay inside the files you own (owners in the README "Team and roles" table). Do not edit another owner's files.
8. Ask before changing `src/config.py` or either contract schema.
9. Never edit or commit `.env`. Never push to or merge into `main`; work on your own branch and open a PR.
10. Dedupe duplicate filings and amendments once, keyed on accession; flag 10b5-1 trades.
