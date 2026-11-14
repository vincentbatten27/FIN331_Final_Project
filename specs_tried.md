# Specifications tried

Log every spec you run, including ones that did not work. One row each, newest last.
Never delete rows.

| Date | Who | Spec (filters, window, benchmark, classification) | Command / script | Output file | Result in one line | Kept? |
|---|---|---|---|---|---|---|
| 2026-11-14 | Vincent | Routine = same calendar month (by trade date) in each of prior 3 years; history = earlier FILINGS only; unclassified if lookback starts before config.V0_HISTORY_START; purchases-only history | `src/classify_insiders.py --sample`; `dev/test_classifier.py` | `data/temp/transactions_classified_sample.csv` (fake data) | Rule implemented and self-tested on a toy history; not yet run on real data | pending |
