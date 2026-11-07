# Audits

One file per check, named `YYYY-MM-DD_<topic>.md`. Each records: what was
checked, how many rows, what was found, and what changed in the pipeline.

Checks the auditors will poke at (do these first):

1. Event date is the filing date, not the trade date.
2. 10b5-1 trades are flagged and handled as documented in the README.
3. Duplicate filings (amendments, joint filings) are removed once.
4. Hand check: sample N random rows with `src/hand_check.py` and compare each
   to the filing on EDGAR.
