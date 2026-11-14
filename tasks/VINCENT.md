# Brief for Vincent (Analyst and CEO), branch `Vincent`

**Goal (Analyst):** classify each purchase as routine or opportunistic, and produce the tables and figure the dashboard reads from `outputs/`. **Goal (CEO):** merge teammates' PRs into `checkpoint-2`, run the audit, and open the single final PR to `main`.

**Read first:** `CLAUDE.md`, `README.md`, and the docstring at the top of each stub.

## Files you own (edit only these)
`src/classify_insiders.py`, `src/report.py`, `src/data_description.py`, `src/hand_check.py`, `specs_tried.md`, `audits/`, `STATUS.md`, `PROPOSAL.md`, `README.md`, `CLAUDE.md`, `src/config.py`.

## Analyst work (you do NOT have to wait for Eric)
Build every script against `data/sample/` first (use the `--sample` flag), then rerun on the real files when Eric's PR lands.
1. **`src/data_description.py`**: done when `outputs/data_description.csv` exists.
2. **`src/classify_insiders.py`**: done when `trade_type` is set using only filings dated before each trade, and a hand check of two insiders matches.
3. **`src/report.py`**: done when `outputs/summary_by_trade_type.csv` (n, mean CAR, std, t-stat) and `outputs/car_by_trade_type.png` exist.
4. **`src/hand_check.py`**: draw random rows with `config.SEED` and compare them to EDGAR by hand; record in `audits/`.
5. **`specs_tried.md`**: log every spec you run, including the ones that fail.

## CEO work, in this order
1. Merge Eric's `transactions.csv` PR first, then rerun your Analyst scripts on real data.
2. Merge Eric's event-study PR and David's app PR into `checkpoint-2`.
3. Clean-clone test: fresh clone, venv, `python run_all.py` rebuilds everything.
4. Run the Skeptical review prompt (Quick Reference #5) on the repo and save its findings.
5. Write by hand: `audits/01_self_audit.md` (what was flagged and what is real; what you fixed and what is open; the 10 checklist items as OK / problem / not yet), `STATUS.md` (3 paragraphs), `PROPOSAL.md`.
6. Open the single PR from `checkpoint-2` to `main` and submit its link on Coursesite.

## Do not
Write the audit write-up, memo or proposal with an agent. The instructor wants them human-written.
