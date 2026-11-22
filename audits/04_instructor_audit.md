# Instructor audit: vincentbatten27, Checkpoint 3

**Repo:** vincentbatten27/FIN331_Final_Project · **Audited commit:** `e3099e5` (2026-11-21 23:11, `main`, merge of PR #13); the CP2 response and README rewrite are on PR #8 (`95e90a8`, 23:09, not merged) · **Seed:** 8, following the insiders · **CP2 audit:** `audits/02_instructor_audit.md` (commit `aeec4ea`)

> Note from your human teacher: This review is generated with minimal supervision from Opus 5.5-high. It is thorough, but can be too generous at times and doesn't know my taste for what is "good". Grades it and I would assign are correlated, but noisy, ok? If you want additional feedback from _me_, you need to find me before/after/during class or during office hours for a guaranteed speedy reply. I will try to respond to emails and issues, but can not respond to student inquiries around the clock across the final weeks of class. Response times will be unpredictable, though during Thanksgiving week, I will do my best to respond quickly virtually, as in person options will be nil.

## Summary

Your response is honest and specific, and both fixes it claims check out. The README now opens with the project, and the EDGAR hand check of all 7 v0 purchases is recorded, and its arithmetic is consistent. The v0 pipeline still reruns from the committed transactions. The dashboard's four pages all render.

But there's no v1. The committed outputs are still v0 (7 purchases, 1 event with returns). The wider all-firm test in `dev/` has 19 events, only 1 of them routine, so the routine-vs-opportunistic comparison the project is about can't be computed yet. Your response says so (B1).

Two smaller items: the fixes on PR #8 aren't on `main` yet (B2). And neither the all-firm test nor anything after it can be rerun without SEC (B3).

## Follow-up on your Checkpoint 2 audit

Response file: `audits/03_audit_response.md` found, on PR #8 (branch `checkpoint-2`, not merged; not on `main`).

| CP2 finding | Status | Evidence |
|---|---|---|
| A1 · CP2 work only on an unmerged PR | fixed | `main` now has the pipeline, `data/output/`, `outputs/` and `audits/01_self_audit.md` (via PRs #11–#13). On PR #8, `README.md` opens with the question and data, and the team instructions moved to `CONTRIBUTING.md`. That README isn't on `main` yet, where `README.md:5` still begins "🚧 Checkpoint 2: what remains (due Sat Nov 14)" (B2) |
| A2 · v0 has one event | disclosed | Response §A2 and the PR #8 README ("That sample has too few events for the routine-vs-opportunistic comparison"). `dev/all_firms_test/summary_by_trade_type.csv`: opportunistic n = 17 (mean CAR 2.43%, t = 1.51), routine n = 1, unclassified n = 1. I recomputed t = 0.02426 / (0.06612/√17) = 1.513. See B1 |
| A3 · Jan-1 membership snapshots | disclosed | PR #8 `README.md:177` ("based on yearly Jan-1 lists, not dated index changes"), with the fix planned in the response |
| A4 · EDGAR hand check not recorded | fixed | PR #8 `audits/hand_check_v0.csv`: 7 rows, one per purchase in `data/output/transactions.csv` (`validate="1:1"`, all 7 matched). `shares × price` reproduces `usd_value_edgar` (max difference $0.0005), `usd_value_ours` equals `transactions.csv`, and `usd_diff_pct` recomputes (max error 4e-5). The EDGAR side wasn't checked here (no SEC requests) |

**2 of 4 fixed, 0 still open (2 disclosed).**

## Checkpoint 3 checks

| Check | Result |
|---|---|
| Reruns from scratch (full sample) | ❌ no full sample (B1). v0: `run_all.py --sample` ("sample contracts: OK"), then `fetch_prices`, `event_study`, `classify_insiders`, `data_description` and `report` rerun from the committed `transactions.csv`. Outputs match (max relative difference 7.9e-7, yfinance drift) |
| Inputs have provenance | ✅ `DATA_SOURCES.md` |
| Keys unique, merges validated | ✅ accession asserted unique |
| No look-ahead / survivorship | ✅ event date = filing date, with after-close filings starting at t = +1 (your hand check confirms the WY case). ⚠️ Jan-1 membership (A3). ⚠️ 44 of 498 firms have no yfinance prices (disclosed) |
| LLM leakage handled | n/a |
| `specs_tried.md` complete | ✅ includes the all-firm test run |
| Magnitudes discussed | ❌ no comparison to size yet (B1) |
| Hand checks | ✅ EDGAR check, 7 of 7 (A4); event-study recompute built in |
| Threats to validity | ✅ README (PR #8), including the yfinance survivorship lean |
| Every number traces to `outputs/` | ⚠️ the response's all-firm numbers trace to `dev/all_firms_test/`, not `outputs/` |
| Dashboard matches `outputs/` | ✅ reads `data/output/transactions.csv` and `outputs/` (v0) |

Steps not rerun by design: `src/fetch_sec.py`, `build_transactions.py` and `dev/test_all_firms.py` (SEC insider data sets; the audit makes no SEC requests). I started from the committed `data/output/transactions.csv`. These are not counted against you.

## Getting ready for Dec 1

Presentations run only from URLs, with a hard cutoff at 9 minutes (10:45 section) or 10 minutes (12:10 section). Put your URL(s) in column G of the Team Projects sheet.

| Check | Result |
|---|---|
| Dashboard launches from a clean clone | ✅ `streamlit run app.py --server.headless true --server.port 8610` (venv from `requirements.txt`) on a clean export of `e3099e5`: `/_stcore/health` returned `ok` after 2 s. A headless browser loaded Home, Intro, Methodology, Results and Explore with no exceptions |
| Dashboard shows the v1 numbers from `outputs/` | ⚠️ it shows the v0 outputs (no v1 yet) |
| README links the live URL(s) | ✅ `README.md:3` links https://fin331-finalproject.streamlit.app/ (the live site itself wasn't checked) |

**Core story for 9–10 minutes:** the Cohen–Malloy–Pomorski question; the classifier (routine = same calendar month in prior years); the routine-vs-opportunistic CAR[+1,+20] with n and t; and today's opportunistic buys (the screener). Data plumbing is one slide.

## What holds up

- **A careful, honest response.** It agrees where the audit was right, doesn't overclaim the +2.4%, and reports new problems the hand check found: the NOC purchase made by a relative (beneficial ownership disclaimed), and the WY after-close timing.
- **The v0 pipeline still reproduces** from the committed transactions, and its data contracts pass (`run_all.py --sample`).
- **The all-firm test shows the classifier produces routine labels on real data** (`trade_types_by_year.csv`: 2021 has 37 opportunistic, 10 routine and 5 unclassified purchases), and shows why 2018–2020 are unclassified: the history starts in 2018 and the rule needs three prior years.

## New findings

### B1 · Blocking · No v1: the main comparison still can't be computed

**Evidence:** `outputs/summary_by_trade_type.csv` (2 rows) and `data/output/event_panel.csv` (20 rows, i.e. one event) are v0. The all-firm test (`dev/all_firms_test/coverage.csv`) found 52 purchases in Jan–Jun 2021, of which 28 pass the filters and 19 have returns. In `summary_by_trade_type.csv` there, routine has n = 1. The response's "Plan for v1 (not done by this deadline)": all S&P 500 firms, filed 2020–2022, with SEC history back to 2017.

**Why it matters:** Checkpoint 3 was v1 on the full sample. Without routine purchases there's no comparison, and the seed's question is unanswered.

**Fix:** Run the v1 plan in the pipeline, not in `dev/`. Use events filed 2020–2022 and history from 2017. Write `outputs/summary_by_trade_type.csv` with n and t for routine and opportunistic, and log the window choice in `specs_tried.md` before seeing the result.

**How to show it's fixed:** `outputs/summary_by_trade_type.csv` has routine and opportunistic rows with n > 1 and t-stats, from the pipeline (`run_all.py`).

### B2 · Minor · The fixes on PR #8 aren't on `main` yet

**Evidence:** At the deadline, `checkpoint-2` (`95e90a8`) is not an ancestor of `main` (`git merge-base --is-ancestor` fails). So `main` lacks the response, `audits/hand_check_v0.csv`, `CONTRIBUTING.md` and the new README, and `main`'s README still opens with the team setup instructions.

**Fix:** Merge PR #8 (resolve against PRs #11–#13).

**How to show it's fixed:** `main` contains `95e90a8` or its successor.

### B3 · Minor · The all-firm test can't be rerun without SEC, and its inputs aren't saved

**Evidence:** `data/raw/` is empty in the repo, and `dev/test_all_firms.py` reads the SEC insider data sets downloaded by `fetch_sec.py`. Only the four summary CSVs in `dev/all_firms_test/` are committed.

**Why it matters:** At v1, every result will depend on that download. Anyone without SEC access can't check `transactions.csv` for the full sample.

**Fix:** Commit the v1 `data/output/transactions.csv` (one row per purchase, from public SEC data) and the classifier history it uses, so steps after `build_transactions` rerun offline, as v0 does now.

**How to show it's fixed:** On a fresh clone, the steps after `build_transactions` reproduce the v1 `outputs/` with no network except yfinance.

## How to respond

This audit is `audits/04_instructor_audit.md` in your repo. Fix what you can, then add `audits/05_audit_response.md`, replying to each **B** finding (no CP2 findings are still open): fixed (the commit), disputed (why), or disclosed as a limitation (where).

There's no separate deadline for this response. Keep working through these until your final deliverables are due: the final repo is audited again then.
