# FIN331 Final Project: Do insider purchases predict returns?

**Dashboard (live):** https://fin331-finalproject.streamlit.app/ · **Proposal:** [PROPOSAL.md](PROPOSAL.md) · **Audits:** [audits/](audits/)

Replication-style study of Cohen, Malloy & Pomorski (2012). Do open-market
purchases by CEOs and CFOs of S&P 500 firms predict abnormal returns, and are
"opportunistic" insiders more informative than "routine" ones? Output is a
Streamlit dashboard showing recent opportunistic purchases next to the
historical CAR of similar trades.

Free data only: SEC insider transactions data sets, yfinance, and the yearly
Jan-1 S&P 500 constituent list in `data/reference/`. No WRDS, no paid data, no API keys.

**Status (Checkpoint 2, v0):** the pipeline runs end to end on a small sample
(10 firms, events filed Jan-Jun 2021). That sample has too few events for the
routine-vs-opportunistic comparison; see `outputs/data_description.csv`,
`outputs/summary_by_trade_type.csv`, the wider all-firm test in
`dev/all_firms_test/`, and the open issues in `audits/`.

## How to run

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows; use source .venv/bin/activate elsewhere
pip install -r requirements.txt
copy .env.example .env            # then set SEC_USER_AGENT="Your Name you@lehigh.edu"
python run_all.py                 # skips steps whose output already exists
python run_all.py --force         # rebuild everything
streamlit run app.py              # dashboard
```

`python run_all.py --sample` only checks the fake files in `data/sample/` against the schemas.
New to the team? See [CONTRIBUTING.md](CONTRIBUTING.md).

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
| 3. S&P 500 membership (yearly Jan-1 lists) | `src/sp500_membership.py` | `data/output/sp500_membership.csv` | Developer |
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

All live in `src/config.py`.

| Choice | Value | Status |
|---|---|---|
| Python | 3.12 | decided |
| v0 sample (Checkpoint 2) | 10 tickers (seed 331) from the Jan-1-2021 S&P 500 list; events filed 2021-01-01 to 2021-06-30 | in use |
| Full-study sample (v1 target) | filings 2020-01-01 to 2022-12-31 (3-year MVP) | planned |
| History for the routine rule | 3 prior years of purchases (v0: from 2018-01-01; full study: from 2017-01-01) | in use |
| Roles | CEO, CFO | decided |
| Event date | filing date | decided (hard rule) |
| Event window | (+1, +20) trading days | decided |
| Estimation window | (-250, -30), at least 120 valid days | in use |
| Benchmark | market model on SPY | in use |
| Size filter | usd_value >= $10,000 | in use |
| 10b5-1 | flagged; excluded from the main spec | in use |
| Routine rule | same calendar month in each of the prior 3 years (Cohen et al.); v0 history is purchases only | in use |
| Seed | 331 | decided |

## Team and roles

| Role | Name | GitHub username | Branch | Owns |
|---|---|---|---|---|
| CEO | Vincent Batten | vincentbatten27 | main (reviews and merges) | this README, `CLAUDE.md`, `STATUS.md`, `PROPOSAL.md`, reviewing every pull request, approving any change to `src/config.py` or the contract schemas |
| Developer | Eric Schneps | ers226-crypto | Eric | data and event-study code: `src/fetch_sec.py`, `src/build_transactions.py`, `src/sp500_membership.py`, `src/fetch_prices.py`, `src/event_study.py`, `run_all.py`, `src/contracts.py`, `DATA_SOURCES.md` |
| Product manager | David | dak728-arch | David | `app.py` and `pages/` (the dashboard), `docs/images/` (mockup) |
| Analyst | Vincent Batten | vab227 | Vincent | `src/classify_insiders.py`, `src/report.py`, `src/data_description.py`, `src/hand_check.py`, `audits/`, `specs_tried.md` (every number has a source and every spec is logged) |

### Workflow

- Nobody pushes to `main`. Work on your own branch and open a pull request.
- The CEO reviews and merges every pull request.
- Stay inside the files you own. If you need a change in someone else's file,
  ask the owner or open an issue.
- `src/config.py` and the two contract schemas are shared. Ask the CEO before
  changing them.
- Log every specification you run in `specs_tried.md`, including failures.
- Never edit or commit `.env`.

## Folder layout

```
src/              code (config.py is shared; one owner per script, see Team and roles)
pages/, app.py    Streamlit dashboard
data/raw/         downloads (git-ignored)
data/temp/        caches / scratch (git-ignored)
data/reference/   small committed inputs (yearly S&P 500 list)
data/output/      contract files passed between steps
data/sample/      fake rows used by the app and for testing
outputs/          every table/figure shown to users, produced by code
audits/           self-audit, instructor audit and response, EDGAR hand check
dev/              tests and scratch work (classifier test, all-firm test run)
tasks/, CONTRIBUTING.md   team setup and per-person briefs
docs/images/      dashboard mockup and screenshot
PROPOSAL.md       project proposal
STATUS.md         Checkpoint 1 memo (what we picked and why)
DATA_SOURCES.md   provenance of every raw input
specs_tried.md    log of every specification run
```

## Threats to validity

- **Sample size:** the v0 sample (10 firms, six months) produced too few events to compare
  routine and opportunistic purchases. A wider test in `dev/all_firms_test/` finds
  more events but few routine ones; the full study needs a longer period.
- **Survivorship:** firms delisted or acquired during the sample may be missing
  from free price data (yfinance), biasing returns upward. The all-firm test lists
  the tickers without prices in `dev/all_firms_test/coverage.csv`.
- **Look-ahead:** the event is dated at the filing date; routine classification
  uses only filings dated before each trade.
- **S&P 500 membership:** based on yearly Jan-1 lists, not dated index changes.
  Additions and removals during a year are misdated, and the v0 universe is drawn
  from the same list used to check it. Planned fix: membership spells from dated
  changes (see `audits/03_audit_response.md`).
- **Overlapping events:** repeated purchases by the same insider or firm within
  20 trading days share return windows, so observations are not independent.
- **10b5-1 plans:** before 2023 the flag comes from footnote and remark text, not a
  structured field, so it can be wrong in either direction.
- **Classification:** a purchase is labelled opportunistic when it is not routine, including an
  insider's first purchase in the data. History is purchases only.
- **Data quality:** the EDGAR hand check (`audits/hand_check_v0.csv`) found one purchase
  that is not an informative insider decision (shares bought by an executive's
  relative) and small rounding differences in `usd_value` (prices are rounded to cents).
