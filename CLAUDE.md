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