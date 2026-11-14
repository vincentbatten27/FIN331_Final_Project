# Brief for Eric (Developer), branch `Eric`

**Goal:** produce the two contract files for the v0 sample: `data/output/transactions.csv` and `data/output/event_panel.csv`.

**Read first:** `CLAUDE.md` (hard rules), `README.md` (schemas, pipeline table), `src/config.py` (all settings), and the docstring at the top of each stub below.

## Files you own (edit only these)
`src/fetch_sec.py`, `src/build_transactions.py`, `src/sp500_membership.py`, `src/fetch_prices.py`, `src/event_study.py`, `run_all.py`, `src/contracts.py`, `DATA_SOURCES.md`.
Do not edit `src/config.py` or the schemas without asking Vincent.

## Your `.env`
Copy `.env.example` to `.env` and type exactly this on the `SEC_USER_AGENT` line (SEC requires a name and email):

```
SEC_USER_AGENT=Eric Schneps ers226@lehigh.edu
```
`.env` is git-ignored. Never commit it or paste it anywhere.

## Do in this order (each step has a "done when")
1. **`src/sp500_membership.py`** (quick, unblocks everything). Done when `data/output/v0_universe.csv` has `config.V0_N_FIRMS` tickers and `sp500_membership.csv` exists.
2. **`src/fetch_sec.py`**. Look up the official SEC insider transactions data set page and its documented file layout; do not use field names from memory. Done when the quarterly zips for `V0_HISTORY_START` to `V0_EVENT_END` are in `data/raw/` and `sec_done.flag` exists.
3. **`src/build_transactions.py`**. **This is the milestone everyone waits on: open a PR into `checkpoint-2` as soon as it works.** Done when `data/output/transactions.csv` exists, `accession` is unique, `trans_date <= filing_date`, and `contracts.validate_transactions` returns no problems.
4. **`src/fetch_prices.py`**. Done when prices for the v0 tickers and SPY are in `data/raw/` and `prices_done.flag` exists. Report any ticker with missing prices.
5. **`src/event_study.py`**. Done when `data/output/event_panel.csv` exists, `(accession, t)` is unique, `contracts.validate_event_panel` returns no problems, and you hand-recomputed one event's CAR and it matches.
6. **`DATA_SOURCES.md`**: fill one row per raw input (source URL, date pulled, code that re-gets it). Do this as you go.

## Check before every PR
- `python run_all.py --sample` prints `sample contracts: OK`.
- `python run_all.py` runs your steps without errors.
- Every merge uses `validate=`. No hard-coded numbers (use `src/config.py`).

## Do not
Fill any data from memory, use the trade date as the event date, edit `.env.example`, or push to `main`.

## When done
Commit, push branch `Eric`, and open a pull request into `checkpoint-2`. Tag Vincent.
