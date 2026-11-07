# FIN331 Final Project: Do insider purchases predict returns?

Replication-style study of Cohen, Malloy & Pomorski (2012). Do open-market
purchases by CEOs and CFOs of S&P 500 firms predict abnormal returns, and are
"opportunistic" insiders more informative than "routine" ones? Output is a
Streamlit dashboard showing recent opportunistic purchases next to the
historical CAR of similar trades.

Free data only: SEC insider transactions data sets, yfinance, Ken French
factors, Wikipedia S&P 500 changes. No WRDS, no paid data, no API keys.

## Team and roles

| Role | Name | GitHub username | Branch | Owns |
|---|---|---|---|---|
| CEO | Vincent Batten | vincentbatten27 | main (reviews and merges) | this README, `CLAUDE.md`, reviewing every pull request, approving any change to `src/config.py` or the contract schemas |
| Developer | Eric | ers226-crypto | dev-pipeline | data and event-study code: `src/fetch_sec.py`, `src/build_transactions.py`, `src/sp500_membership.py`, `src/fetch_prices.py`, `src/event_study.py`, `run_all.py`, `src/contracts.py` |
| Product manager | David | dak728-arch | pm-app | `app.py` (the dashboard), `STATUS.md` |
| Analyst | Vincent Batten | vab227 | analyst-classify | `src/classify_insiders.py`, `src/report.py`, `src/hand_check.py`, `audits/`, `specs_tried.md` (every number has a source and every spec is logged) |

### Workflow

- Nobody pushes to `main`. Work on your own branch and open a pull request.
- The CEO reviews and merges every pull request.
- Stay inside the files you own. If you need a change in someone else's file,
  ask the owner or open an issue.
- `src/config.py` and the two contract schemas are shared. Ask the CEO before
  changing them.
- Log every specification you run in `specs_tried.md`, including failures.
- Never edit or commit `.env`.

## Unit of observation

One row = one insider open-market purchase (Form 4, code P), identified by
`accession` + insider. The event date is the **filing date** (the day the
purchase became public), never the trade date. Outcome: CAR[+1,+20] in trading
days after the filing date.

Fake example rows (see `data/sample/`; tickers are `FAKEn`, not real firms):

| accession | ticker | role | filing_date | trans_date | usd_value | is_10b5_1 | trade_type | car_1_20 |
|---|---|---|---|---|---|---|---|---|
| 0000000000-21-000001 | FAKE1 | CFO | 2021-02-01 | 2021-01-27 | 25000 | 0 | routine | -0.0178 |
| 0000000000-21-000002 | FAKE2 | CEO | 2021-02-18 | 2021-02-17 | 150000 | 0 | opportunistic | -0.0078 |
| 0000000000-21-000003 | FAKE3 | CFO | 2021-03-08 | 2021-03-04 | 400000 | 0 | unclassified | (not in sample panel) |

`car_1_20` is not stored in `transactions.csv`; it is derived from
`event_panel.csv` (CAR at t=20) in the analysis step. The sample panel stops at
t=6 for brevity, so those two values are the t=6 CAR.

## Pipeline

Script names are the planned names. Each owner creates and maintains their own
scripts (see Team and roles).

| Step | Script | Output | Owner |
|---|---|---|---|
| 1. Download SEC insider data sets | `src/fetch_sec.py` | `data/raw/` | Developer |
| 2. Build purchase table (dedupe, filing date, 10b5-1 flag) | `src/build_transactions.py` | `data/output/transactions.csv` | Developer |
| 3. Point-in-time S&P 500 membership | `src/sp500_membership.py` | `data/output/sp500_membership.csv` | Developer |
| 4. Prices, market proxy, factors | `src/fetch_prices.py` | `data/raw/` | Developer |
| 5. Event study (market model, AR, CAR) | `src/event_study.py` | `data/output/event_panel.csv` | Developer |
| 6. Routine / opportunistic classification | `src/classify_insiders.py` | `trade_type` in `transactions.csv` | Analyst |
| 7. Tables and figures | `src/report.py` | `outputs/` | Analyst |
| 8. Dashboard | `app.py` | (reads `outputs/`; sample data until real files exist) | Product manager |
| Hand check of random rows vs. EDGAR | `src/hand_check.py` | `audits/` | Analyst (everyone helps check) |

## Contract schemas

Steps communicate only through these two files. Ask the CEO before changing
a column.

### `transactions.csv` (one row per purchase)

| Column | Type | Meaning |
|---|---|---|
| accession | str | SEC accession number of the Form 4 filing |
| issuer_cik | int | CIK of the issuing company |
| ticker | str | Issuer ticker at filing time |
| insider_cik | int | CIK of the reporting insider |
| role | str | One of `config.ROLES` (CEO, CFO) |
| filing_date | date | Date the filing was accepted by the SEC (the event date) |
| trans_date | date | Date of the trade (information only, never the event date) |
| usd_value | float | Shares x price paid, USD |
| is_10b5_1 | 0/1 | Trade made under a 10b5-1 plan |
| trade_type | str | `routine`, `opportunistic`, or `unclassified` (too little history) |

### `event_panel.csv` (one row per event x trading day)

| Column | Type | Meaning |
|---|---|---|
| accession | str | Key back to `transactions.csv` |
| ticker | str | Ticker |
| filing_date | date | Event date |
| t | int | Trading days relative to filing date (event window is `config.EVENT_WINDOW`) |
| date | date | Calendar date of day t |
| ret | float | Stock return on `date` |
| mkt | float | Market proxy return on `date` |
| expected | float | Market-model expected return (parameters estimated over `config.ESTIMATION_WINDOW`) |
| AR | float | `ret - expected` |
| CAR | float | Cumulative AR from `t = EVENT_WINDOW[0]` through `t` |

## Choices

All live in `src/config.py`. "Proposed" = default awaiting CEO sign-off.

| Choice | Value | Status |
|---|---|---|
| Python | 3.12 | decided |
| Sample period (filing dates) | 2020-01-01 to 2022-12-31 (3-year MVP) | proposed |
| History for routine rule | from 2017-01-01 | proposed |
| Roles | CEO, CFO | decided |
| Event date | filing date | decided (hard rule) |
| Event window | (+1, +20) | decided |
| Estimation window | (-250, -30), min 120 valid days | proposed (min days) |
| Benchmark | market model on SPY | proposed |
| Size filter | usd_value >= $10,000 | proposed |
| 10b5-1 | flagged; excluded from main spec | proposed |
| Routine rule | same calendar month in each of the prior 3 years (Cohen et al.) | proposed |
| Seed | 331 | decided |

## How to run

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows; use source .venv/bin/activate elsewhere
pip install -r requirements.txt
copy .env.example .env            # then set SEC_USER_AGENT="Your Name you@lehigh.edu"
python run_all.py                 # skips steps whose output already exists
python run_all.py --force         # rebuild everything
streamlit run app.py              # dashboard (sample data until real outputs exist)
```

## Folder layout

```
src/          code (config.py is shared; one owner per script, see Team and roles)
data/raw/     downloads (git-ignored)
data/temp/    caches / scratch (git-ignored)
data/output/  contract files passed between steps
data/sample/  fake rows used by the app and for testing
outputs/      every table/figure shown to users, produced by code
audits/       hand-check notes and results
dev/          scratch work not part of the pipeline
STATUS.md     who is doing what, what is blocked
specs_tried.md  log of every specification run
```

## Threats to validity

- **Survivorship:** firms delisted or acquired during the sample may be missing
  from free price data (yfinance), biasing returns upward.
- **Look-ahead:** the event is dated at the filing date; routine classification
  uses only trades before each trade; S&P membership must be as of the event.
- **Overlapping events:** repeated purchases by the same insider or firm within
  20 trading days share return windows, so observations are not independent.
- **10b5-1 plans:** planned trades carry no new information; flagged by
  `is_10b5_1`, and the flag is only reliable in recent filings.
- **S&P 500 membership:** reconstructed from Wikipedia change tables and yearly
  Jan-1 lists, not a vendor point-in-time file; mid-year additions/removals and
  ticker reuse can be misdated.
