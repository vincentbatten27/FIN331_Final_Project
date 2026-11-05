# STATUS

Update your row when you start, finish, or get blocked.

| Lane | Owner | Scope | Status | Blocked on |
|---|---|---|---|---|
| A: data | TBD | SEC data sets, `transactions.csv`, S&P membership | not started | |
| B: event study | TBD | prices, market model, `event_panel.csv` | not started | |
| C: classification + dashboard | TBD | routine/opportunistic, `outputs/`, `app.py` | not started | |

## Open decisions (proposed defaults in README "Choices")

- Sample period, min estimation days, benchmark, size filter, 10b5-1 handling, routine rule.
- Where to keep the yearly S&P 500 list (`spx_yearly_tickers.csv`) so all three can use it.
