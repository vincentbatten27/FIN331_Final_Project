"""Step 1: download the SEC insider transactions data sets.

Owner: Developer (Eric).

Inputs : SEC insider transactions data sets (quarterly zips), listed on
         DATASETS_PAGE. Field layout: the SEC readme (README_URL), saved to
         data/raw/docs/ alongside the zips.
Output : zips in data/raw/ for every quarter from config.V0_HISTORY_START to
         config.V0_EVENT_END, then write data/raw/sec_done.flag.
Needs  : config.sec_user_agent() (set SEC_USER_AGENT in .env; never commit .env).
Rules  : skip files already downloaded; record source URL and date pulled in
         DATA_SOURCES.md.

Zip URLs are read from the data sets page rather than built by hand, because the
SEC has moved newer quarters to a different folder.

Rules: event date is the filing date; never fill data from memory (look up
file layouts in the official documentation); no hard-coded numbers (use
src/config.py); keep the contract columns in README.md exactly; log any spec you
try in specs_tried.md.
"""
import re
import sys
import time
import zipfile
from datetime import date

import pandas as pd
import requests

import config

SEC = "https://www.sec.gov"
DATASETS_PAGE = SEC + "/data-research/sec-markets-data/insider-transactions-data-sets"
README_URL = SEC + "/files/insider_transactions_readme.pdf"
DOCS_DIR = config.DATA_RAW / "docs"
FLAG = config.DATA_RAW / "sec_done.flag"
PAUSE = 0.5  # seconds between requests; the SEC asks for at most 10 per second


def quarters(start: date, end: date) -> list[str]:
    """Quarter labels like '2018q1' covering start..end."""
    periods = pd.period_range(pd.Timestamp(start), pd.Timestamp(end), freq="Q")
    return [f"{p.year}q{p.quarter}" for p in periods]


def zip_links(session: requests.Session) -> dict[str, str]:
    """{'2021q1': absolute URL} for every zip linked on the data sets page."""
    html = session.get(DATASETS_PAGE, timeout=60)
    html.raise_for_status()
    hrefs = re.findall(r'href="([^"]*?(\d{4}q[1-4])_form345\.zip)"', html.text)
    return {q: (h if h.startswith("http") else SEC + h) for h, q in hrefs}


def download(session: requests.Session, url: str, dest) -> None:
    """Stream url to dest via a temp file, so an interrupted download is never kept."""
    tmp = dest.with_suffix(dest.suffix + ".part")
    with session.get(url, stream=True, timeout=300) as r:
        r.raise_for_status()
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(1 << 20):
                f.write(chunk)
    tmp.rename(dest)
    time.sleep(PAUSE)


def main() -> None:
    config.DATA_RAW.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers.update({"User-Agent": config.sec_user_agent()})

    readme = DOCS_DIR / "insider_transactions_readme.pdf"
    if not readme.exists():
        download(session, README_URL, readme)

    links = zip_links(session)
    wanted = quarters(config.V0_HISTORY_START, config.V0_EVENT_END)
    missing = [q for q in wanted if q not in links]
    if missing:
        sys.exit(f"No zip linked on {DATASETS_PAGE} for: {', '.join(missing)}. Stopping.")

    for q in wanted:
        dest = config.DATA_RAW / f"{q}_form345.zip"
        if dest.exists() and zipfile.is_zipfile(dest):
            print(f"{dest.name}: already downloaded")
            continue
        print(f"{dest.name}: downloading {links[q]}")
        download(session, links[q], dest)
        if not zipfile.is_zipfile(dest):
            dest.unlink()
            sys.exit(f"{dest.name}: not a valid zip (the SEC may have blocked the request). Stopping.")

    FLAG.write_text(f"pulled {date.today()} from {DATASETS_PAGE}\nquarters: {', '.join(wanted)}\n")
    print(f"done: {len(wanted)} quarters in {config.DATA_RAW}")


if __name__ == "__main__":
    main()
