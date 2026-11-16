# Instructor audit: FIN331 insider purchases (vincentbatten27), Checkpoint 2

**Repo:** vincentbatten27/FIN331_Final_Project · **Audited commit:** `aeec4ea` (2026-11-14 23:57, tip of PR #8 `checkpoint-2`, not merged) · **Seed:** 8, following the insiders

> Note from your human teacher: This review is generated with minimal supervision from Opus 5.5-high. It is thorough, but can be too generous at times and doesn't know my taste for what is "good". Grades it and I would assign are correlated, but noisy, ok? If you want additional feedback from _me_, you need to find me before/after/during class or during office hours for a guaranteed speedy reply. I will try to respond to emails and issues, but can not respond to student inquiries around the clock across the final weeks of class. Response times will be unpredictable, though during Thanksgiving week, I will do my best to respond quickly virtually, as in person options will be nil.

## Summary

The design follows the seed closely: filing date not trade date, a 10b5-1 flag, duplicate and amended filings collapsed, and a routine/opportunistic rule that uses only earlier filings. The steps that don't need SEC downloads reproduce your committed outputs. My independent recomputation of the one event study matches exactly. Two problems stand out:
1. The work sits on an unmerged branch (A1).
2. v0 produced **one** event, so the routine-vs-opportunistic comparison, the project's core result, doesn't exist yet even at pilot scale (A2).

| Check | Result |
|---|---|
| Reruns from scratch | ⚠️ `run_all.py --sample`: OK. `fetch_prices`, `event_study`, `classify_insiders`, `data_description` and `report` rerun on the committed `transactions.csv` reproduce the outputs. The SEC download steps weren't run in the audit environment |
| Inputs have provenance | ✅ `DATA_SOURCES.md` |
| Keys unique, merges validated | ✅ accession asserted unique |
| No look-ahead / survivorship | ✅ event date = filing date. ⚠️ index membership from Jan-1 snapshots (your self-audit) |
| LLM leakage handled | n/a |
| `specs_tried.md` complete | ✅ 4 entries matching the code |
| Magnitudes discussed | ❌ one event (A2) |
| Hand checks | ⚠️ the event-study recompute is built in. `hand_check.py` draws 7 rows to check on EDGAR, but no results are recorded |
| Threats to validity | ✅ README section |
| Every number traces to `outputs/` | ✅ |

## What holds up

- **Event study recomputed independently.** WY, CFO purchase filed 2021-05-06. My code (fresh yfinance, day 0 = first trading day on or after the filing date, market model on SPY over trading days −250 to −30, CAR over +1 to +20) gives alpha 0.00076, beta 1.551, 221 estimation days, CAR −0.106452. Identical to `specs_tried.md` and `outputs/summary_by_trade_type.csv`.
- **Rerun:** with the committed `transactions.csv`, the regenerated `summary_by_trade_type.csv` and `data_description.csv` are identical. `event_panel.csv` differs by under 1e-6 per return (yfinance float drift); the CAR is unchanged to 6 decimals.
- **Seed 8, transaction vs. filing date:** the filing date is used throughout.
- **Seed 8, 10b5-1:** detected from footnotes and remarks, since the structured flag only exists from 2023. You validated the detector on sales (2 of 6 flagged).
- **Seed 8, duplicates:** a purchase reported in several filings or a 4/A is kept once (earliest filing).

## Findings

### A1 · Major · The Checkpoint 2 work is only on an unmerged pull request

**Evidence:**
- `main` at the deadline (`bbf7eca`, 23:57:04) has `PROPOSAL.md` but no `audits/01_self_audit.md`.
- The self-audit, the real data outputs and the pipeline code (25 files, +1,142 lines vs. `main`) are on `checkpoint-2` (PR #8, `aeec4ea`, 23:57:31), which is not merged.
- PR #6 (Eric) and PR #7 (David) are also open.
- The README's top section is still the team's setup instructions ("Your job is in your brief", agent prompts A–C) rather than a description of the project.

**Fix:** Merge PR #8 (and #6/#7 once reviewed) into `main`. Move the onboarding prompts to `tasks/` or `CONTRIBUTING.md`, so the README opens with the question, how to run, and the threats.

**How to show it's fixed:** `main` contains the self-audit and the outputs, and the README starts with the project.

### A2 · Major · v0 has one event, so the main comparison can't be computed

**Evidence:**
- `outputs/data_description.csv`: 7 purchases, `n_events_with_returns` = 1, `n_trade_type_opportunistic` = 1, `n_trade_type_unclassified` = 6, no routine trades.
- `outputs/summary_by_trade_type.csv`: n = 1 with no SE or t.
- The v0 scope (`src/config.py`; README "Facts everyone needs") is 10 tickers with events filed 2021-01-01 to 2021-06-30.

**Why it matters:** The pipeline technically runs end to end. But the classifier, the core of the project, has never produced a routine trade on real data, so you can't yet tell whether it works. Insider purchases by S&P 500 CEOs and CFOs are rare: about one per firm-decade in your sample.

**Fix:** For v1, use the seed's MVP: all S&P 500 firms, CEO/CFO purchases, about 3 years of events, with history back far enough for the 3-year routine rule. Before that, widen v0 (e.g. 50 tickers, events 2019–2021) until both trade types appear, and report the classification counts by year.

**How to show it's fixed:** `summary_by_trade_type.csv` has rows for routine and opportunistic with n > 1 and t-stats.

### A3 · Minor · Index membership uses Jan-1 snapshots

**Evidence:** `data/reference/spx_yearly_tickers.csv` (yearly snapshots), used by `src/sp500_membership.py`. Your self-audit: "problem for membership (Jan-1 snapshots)".

**Why it matters:** Firms added during the year are missed until the next January, and firms removed during the year stay in. Small for v0, but it will matter at full scale.

**Fix:** Build membership spells from the dated index changes (add/remove dates), and test membership on the filing date.

**How to show it's fixed:** `sp500_membership.csv` has start and end dates per ticker.

### A4 · Minor · The EDGAR hand check isn't recorded

**Evidence:** `src/hand_check.py` writes 7 sampled rows to `audits/hand_check_sample.csv` (ran OK). No completed comparison against the filings exists, and your self-audit says "not yet for transactions and the classifier on EDGAR".

**Fix:** For each sampled row, open the Form 4 on EDGAR and record role, trade date, filing date, shares, price and 10b5-1 status next to your values, with a match column.

**How to show it's fixed:** A completed `audits/hand_check_v0.csv` with a match rate.

## How to respond

This audit is `audits/02_instructor_audit.md` in your repo. Fix what you can, then add `audits/03_audit_response.md`, replying to each finding ID: fixed (the commit), disputed (why), or disclosed as a limitation (where).

**Deadline: Saturday, November 21, 2026.**
