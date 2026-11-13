# FIN331 Final Project: Do insider purchases predict returns?

**Dashboard (live):** _link goes here once David deploys it_

## 🚧 Checkpoint 2: what remains (due Sat Nov 14)

**Start here (everyone):**
1. `git fetch`, then `git checkout checkpoint-2`, then `git checkout -b <your branch>`.
2. Create the venv, `pip install -r requirements.txt`, copy `.env.example` to `.env` and set `SEC_USER_AGENT`.
3. Open your coding agent at the repo root. Tell it to read `CLAUDE.md` and this README, then paste your prompt below.
4. Edit ONLY your own files. Open a PR into `checkpoint-2` and tag Vincent.

**v0 scope (proposed, in `src/config.py`):** 10 tickers drawn with seed 331 from the Jan-1-2021 S&P 500 list in `data/reference/`, events filed 2021-01-01 to 2021-06-30, history from 2018-01-01.

**Agreed output files** (`outputs/`; the Analyst writes them, the app reads them): `data_description.csv`, `summary_by_trade_type.csv`, `car_by_trade_type.png`.

**Who waits on whom:** nobody has to wait. The app and the Analyst scripts build against `data/sample/` until Eric's real files land, then switch over. Eric's `transactions.csv` unblocks the real Analyst run, and his `event_panel.csv` unblocks real results in the app.

### Eric (Developer), branch `dev-pipeline`
- [ ] `DATA_SOURCES.md`: fill one row per raw input (source, date pulled, code that re-gets it)
- [ ] `src/fetch_sec.py` and `src/build_transactions.py` write `data/output/transactions.csv`. DO THIS FIRST.
- [ ] `src/sp500_membership.py`, `src/fetch_prices.py`, `src/event_study.py` write `data/output/event_panel.csv`
- [ ] Wire every step into `run_all.py`
> **Agent prompt:** Read CLAUDE.md and the README contract schemas. Build the Developer-owned scripts for the v0 scope in src/config.py. Event date is the filing date. Assert accession is unique and use validate= on every merge. Never fill data from memory. Edit only my files.

### David (Product manager), branch `pm-app`
- [ ] `docs/images/dashboard_mockup.png`: an Excalidraw sketch of the finished dashboard. Do this first.
- [ ] `app.py` plus `pages/1_Intro.py`, `pages/2_Methodology.py`, `pages/3_Results.py`, `pages/4_Explore.py`, reading `outputs/` and falling back to `data/sample/`
- [ ] Deploy on Streamlit Community Cloud, then put the link at the top of this README
> **Agent prompt:** Read CLAUDE.md and the README. Build the four-page Streamlit app reading only from outputs/ or data/sample/. No hard-coded numbers. Edit only app.py and pages/.

### Vincent (Analyst), branch `analyst-classify`
- [ ] `src/data_description.py` writes `outputs/data_description.csv`
- [ ] `src/classify_insiders.py` (routine vs opportunistic, no look-ahead)
- [ ] `src/report.py` writes `outputs/summary_by_trade_type.csv` and `outputs/car_by_trade_type.png`
- [ ] `src/hand_check.py` and `specs_tried.md` (log every spec)
> **Agent prompt:** Read CLAUDE.md and the README. Build the Analyst-owned scripts against data/sample/ first, then the real files. Use only information available before each trade. Log every spec in specs_tried.md.

### Vincent (CEO) and everyone
- [ ] `STATUS.md` memo, written by hand
- [ ] Merge PRs into `checkpoint-2`, test `run_all.py` on a clean clone, open the single PR to `main`
- [ ] Run the Skeptical review prompt, then write `audits/01_self_audit.md` by hand
- [ ] `PROPOSAL.md`, written by hand, last

---

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
| CEO | Vincent Batten | vincentbatten27 | main (reviews and merges) | this README, `CLAUDE.md`, `STATUS.md`, `PROPOSAL.md`, reviewing every pull request, approving any change to `src/config.py` or the contract schemas |
| Developer | Eric | ers226-crypto | dev-pipeline | data and event-study code: `src/fetch_sec.py`, `src/build_transactions.py`, `src/sp500_membership.py`, `src/fetch_prices.py`, `src/event_study.py`, `run_all.py`, `src/contracts.py` |
| Product manager | David | dak728-arch | pm-app | `app.py` and `pages/` (the dashboard), `docs/images/` (mockup) |
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
data/reference/ small committed inputs (yearly S&P 500 list)
data/output/  contract files passed between steps
data/sample/  fake rows used by the app and for testing
outputs/      every table/figure shown to users, produced by code
audits/       hand-check notes and results
dev/          scratch work not part of the pipeline
STATUS.md     Checkpoint 1 memo (what we picked and why)
DATA_SOURCES.md  provenance of every raw input
dev/TASKS.md  team task tracker
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
