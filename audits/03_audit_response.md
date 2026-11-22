# Response to the instructor audit of Checkpoint 2

Responds to [`02_instructor_audit.md`](02_instructor_audit.md) (audited commit `aeec4ea`). Each finding is marked **fixed**, **disputed** or **disclosed as a limitation**.

| ID | Severity | Response | Evidence |
|---|---|---|---|
| A1 | Major | Fixed (once PR #8 is merged into `main`) | `README.md`, `CONTRIBUTING.md`, PR #8 |
| A2 | Major | Disclosed as a limitation; partly addressed by a wider test run | `dev/all_firms_test/`, `specs_tried.md` |
| A3 | Minor | Disclosed as a limitation; fix planned | `README.md` (Threats), this file |
| A4 | Minor | Fixed | `audits/hand_check_v0.csv` |

## A1 · The Checkpoint 2 work is only on an unmerged pull request

**Response: fixed.** We agree with the finding. At the deadline the work was on `checkpoint-2` (PR #8) and `main` had only the proposal and a draft audit.

What changed:
- PR #8 (`checkpoint-2` into `main`) is merged, so `main` contains the pipeline code, the real v0 outputs, the dashboard, the proposal, the self-audit (`audits/01_self_audit.md`), the instructor audit and this response.
- The README now opens with the question, the data, how to run, and the threats. The team setup instructions (agent prompts A, B and C) moved to `CONTRIBUTING.md`.
- The README's Choices, Pipeline and Threats sections now match the code. For example, step 3 is labelled as yearly Jan-1 lists, not point-in-time membership, and the Wikipedia change tables are no longer described as a source we use.

**Still open:** none for this finding.

## A2 · v0 has one event, so the main comparison can't be computed

**Response: disclosed as a limitation, with a wider test run as partial progress.** We agree that the v0 sample (10 firms, events filed 2021-01-01 to 2021-06-30) has one event with returns, so the routine-versus-opportunistic comparison cannot be computed on the committed outputs. The README and the proposal say so.

What we ran since the audit (Eric, `dev/test_all_firms.py`, logged in `specs_tried.md`): the same v0 specification on all 498 firms on the Jan-1-2021 S&P 500 list, same filing window. This is a test run; `config.py` and the committed `data/output/` files were not changed. Results are in `dev/all_firms_test/`:
- `coverage.csv`: 52 CEO/CFO purchases filed in the window, 28 pass the size and 10b5-1 filters, 19 have return data (9 dropped because yfinance has no prices for those tickers).
- `trade_types_by_year.csv`: the classifier labels, by filing year. In 2021 there are 37 opportunistic, 10 routine and 5 unclassified purchases. In 2018 to 2020 every purchase is unclassified, because the history only starts in 2018 and the rule needs three prior years.
- `summary_by_trade_type.csv`: of the 19 events with returns, 17 are opportunistic (mean CAR[+1,+20] about +2.4%, t about 1.5), 1 is routine and 1 is unclassified.

What this shows and does not show:
- The classifier now produces routine labels on real data, which v0 could not show.
- The comparison the project is about is still not computable: with one routine event among the 19, there is nothing to compare against. We are not drawing a conclusion from the +2.4%.
- The test run lives in `dev/`, not in the pipeline outputs, and the dashboard still shows v0.

**Plan for v1 (not done by this deadline):** all S&P 500 firms, about three years of events (filed 2020 to 2022), with SEC history back to 2017 so that the first events can be classified. We will report the classification counts by year, and routine and opportunistic CARs with n and t-statistics in `summary_by_trade_type.csv`, as the audit asks.

**Related risk, disclosed:** in the all-firm test, 44 tickers have no yfinance prices (`coverage.csv`), and 9 of the 28 eligible events were dropped for that reason. Missing prices are concentrated in firms that were acquired or delisted, so the sample leans toward survivors. This is in the README threats.

## A3 · Index membership uses Jan-1 snapshots

**Response: disclosed as a limitation; fix planned.** We agree. Membership comes from yearly Jan-1 lists in `data/reference/spx_yearly_tickers.csv`, so firms added or removed during a year are misdated. In v0 the 10 firms are drawn from the same Jan-1-2021 list used to check the events, so the check passes by construction.

Correction to our earlier self-audit: it said a Wikipedia scraper existed in rough draft form. No such scraper is in the repo yet. It is planned, not built.

**Plan:** build membership spells (start and end date per ticker) from dated index changes, test membership on the filing date, and rebuild the sample universe per year instead of from one list. Not done by this deadline. Until then the README threats section describes the limitation, and the proposal wording was changed to say membership is as of January 1st of the filing year.

## A4 · The EDGAR hand check isn't recorded

**Response: fixed.** All 7 purchases in `data/output/transactions.csv` were opened on EDGAR (each filing's full-text submission page) and compared field by field. The result is `audits/hand_check_v0.csv`.

Match rate, 7 purchases:
- Role (CEO or CFO), trade date, filing date, and the 10b5-1 flag agree in **7 of 7**.
- `usd_value` equals shares times price on EDGAR exactly in 3 of 7, and within 0.011% in all 7. The differences come from prices rounded to cents in our data (for example EDGAR price 32.9992, our value implies 33.00). This is immaterial but we note it.
- No duplicate filings among the 7.

New findings from the hand check:
- **One purchase is not an informative insider decision.** The NOC row (`0001225208-19-004964`) matches the filing, but footnote F1 says the shares were owned by the executive's mother, bought and sold without his knowledge, and he disclaims beneficial ownership. It is a history row (filed 2019), so it affects only that insider's classification, not the event sample. At scale we need a review step that flags filings whose footnotes disclaim beneficial ownership. Not built yet.
- **After-close filings are handled as intended.** The WY event (`0001209191-21-030636`) was accepted at 4:41pm ET on 2021-05-06, after the close. The event window starts at t = +1, which is the next trading day, so the first reaction day is included.

How it was checked: an AI agent read the EDGAR pages and recorded the fields; the team should re-check two or three rows by eye before relying on it.

**Still open:** the check covers v0's 7 purchases only. A larger sample is needed for v1, using `src/hand_check.py` to draw the rows.
