"""Step 1: download the SEC insider transactions data sets.

Owner: Developer (Eric). STATUS: STUB, not implemented yet.

Inputs : SEC insider transactions data sets (quarterly zips). Find the official
         page and file layout in the SEC documentation; do not recall field names.
Output : zips in data/raw/ for every quarter from config.V0_HISTORY_START to
         config.V0_EVENT_END, then write data/raw/sec_done.flag.
Needs  : config.sec_user_agent() (set SEC_USER_AGENT in .env; never commit .env).
Rules  : skip files already downloaded; record source URL and date pulled in
         DATA_SOURCES.md.

Rules: event date is the filing date; never fill data from memory (look up
file layouts in the official documentation); no hard-coded numbers (use
src/config.py); keep the contract columns in README.md exactly; log any spec you
try in specs_tried.md.
"""
import sys

import config  # noqa: F401  (all paths and parameters come from src/config.py)


def main() -> None:
    print("fetch_sec.py: stub, not implemented yet")
    sys.exit(2)  # exit code 2 = "not implemented"; run_all.py reports it as such


if __name__ == "__main__":
    main()
