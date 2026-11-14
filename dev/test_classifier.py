"""Self-test for src/classify_insiders.py on a hand-built toy history.

Run:  python dev/test_classifier.py
Checks routine / opportunistic / unclassified labels and that later filings never
change an earlier trade's label (no look-ahead).
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from classify_insiders import classify  # noqa: E402


def row(acc, insider, trans, filed):
    return dict(accession=acc, insider_cik=insider,
                trans_date=pd.Timestamp(trans), filing_date=pd.Timestamp(filed))


HISTORY_START = "2018-01-01"
rows = [
    # insider 1: buys every November 2018-2021 -> the Nov 2021 trade is routine
    row("a18", 1, "2018-11-05", "2018-11-07"),
    row("a19", 1, "2019-11-04", "2019-11-06"),
    row("a20", 1, "2020-11-03", "2020-11-05"),
    row("a21", 1, "2021-11-02", "2021-11-04"),
    # insider 2: bought in 2018 and 2020 only, then Nov 2021 -> opportunistic
    row("b18", 2, "2018-11-05", "2018-11-07"),
    row("b20", 2, "2020-11-03", "2020-11-05"),
    row("b21", 2, "2021-11-02", "2021-11-04"),
    # insider 3: first trade in Jan 2019, lookback reaches before the data -> unclassified
    row("c19", 3, "2019-01-10", "2019-01-12"),
]
tx = pd.DataFrame(rows)
labels = classify(tx, 3, HISTORY_START)
got = dict(zip(tx["accession"], labels))
expected = {"a18": "unclassified", "a19": "unclassified", "a20": "unclassified",
            "a21": "routine", "b21": "opportunistic", "c19": "unclassified"}
for acc, want in expected.items():
    assert got[acc] == want, (acc, got[acc], want)

# No look-ahead: dropping everything filed after the Nov 2021 trade changes nothing.
later = pd.concat([tx, pd.DataFrame([row("a22", 1, "2022-11-01", "2022-11-03")])], ignore_index=True)
assert classify(later, 3, HISTORY_START).loc[tx.index[tx["accession"] == "a21"][0]] == "routine"

# A filing dated after the trade must not make it routine.
fake = pd.DataFrame([
    row("d21", 4, "2021-11-02", "2021-11-04"),
    row("d18", 4, "2018-11-05", "2021-12-01"),   # filed late, after the trade
    row("d19", 4, "2019-11-04", "2021-12-01"),
    row("d20", 4, "2020-11-03", "2021-12-01"),
])
assert classify(fake, 3, HISTORY_START)[0] == "opportunistic"
print("classifier self-test passed")
