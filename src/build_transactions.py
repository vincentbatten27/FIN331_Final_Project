"""Step 2: build the purchase table (data/output/transactions.csv).

Owner: Developer (Eric).

Inputs : the zips in data/raw/, data/output/v0_universe.csv (step 3).
Output : config.TRANSACTIONS_CSV with exactly the columns in README.md.
Do     : keep open-market purchases only (config.TRANSACTION_CODE), insiders whose
         role is in config.ROLES, filing dates from config.V0_HISTORY_START to
         config.V0_EVENT_END (history rows are needed by the routine rule). Dedupe
         by accession. Take filing_date from the filing, not the trade.
         Set is_10b5_1 from the filing's own flag. Write trade_type = "unclassified"
         (the Analyst fills it in step 6). usd_value = shares x price.
Checks : assert accession is unique; assert trans_date <= filing_date;
         run contracts.validate_transactions on the output.

Field names follow the SEC readme (data/raw/docs/insider_transactions_readme.pdf):
SUBMISSION, REPORTINGOWNER, NONDERIV_TRANS and FOOTNOTES, joined on ACCESSION_NUMBER.

Choices (logged in specs_tried.md):
  * Firms are matched by issuer CIK. The CIK for each v0 ticker is taken from its
    filings in the event window, so history rows survive later symbol changes.
  * role comes from RPTOWNER_TITLE: CEO = "CEO" / "Chief Executive Officer", CFO =
    "CFO" / "Chief Financial Officer". Division heads ("CEO-LKQ Europe") are not
    the company CEO. If a title has both, CEO wins.
  * Duplicate filings and amendments: a purchase (issuer, insider, trade date,
    shares, price) reported in more than one filing is kept once, from the
    earliest filing.
  * One row per accession: the purchases in a filing are summed into usd_value and
    trans_date is the earliest trade date in the filing.
  * is_10b5_1: the SUBMISSION file only carries AFF10B5ONE in 2023 and later data
    sets, so for earlier filings the flag is 1 when a footnote attached to the
    purchase, or the filing's remarks, mentions Rule 10b5-1.
"""
import re
import zipfile

import pandas as pd

import config
import contracts
import sp500_membership

SEC_DATE = "%d-%b-%Y"  # DD-MON-YYYY, per the SEC readme
CEO_RE = re.compile(r"\bCEO\b(?!\s*-)|chief\s+executive\s+officer", re.I)
CFO_RE = re.compile(r"\bCFO\b(?!\s*-)|chief\s+financial\s+officer", re.I)
RULE_10B5_1_RE = re.compile(r"10b5-?1", re.I)
FOOTNOTE_ID_RE = re.compile(r"F\d+")


def read_table(zf: zipfile.ZipFile, name: str, usecols=None) -> pd.DataFrame:
    """One tab-delimited table from a quarterly zip, every column as text."""
    with zf.open(f"{name}.tsv") as f:
        return pd.read_csv(f, sep="\t", dtype=str, usecols=usecols, keep_default_na=False,
                           quoting=3, encoding="utf-8")


def role_from_title(title: str):
    if CEO_RE.search(title or ""):
        return "CEO"
    if CFO_RE.search(title or ""):
        return "CFO"
    return None


def load_quarter(path, ciks_by_ticker: dict) -> pd.DataFrame:
    """Purchase rows (one per transaction x CEO/CFO owner) from one quarterly zip."""
    universe = set(ciks_by_ticker)
    with zipfile.ZipFile(path) as zf:
        sub = read_table(zf, "SUBMISSION")
        sub["symbol"] = sub["ISSUERTRADINGSYMBOL"].str.strip().str.upper()
        sub["ISSUERCIK"] = sub["ISSUERCIK"].astype(int)
        sub = sub[sub["symbol"].isin(universe) | sub["ISSUERCIK"].isin(ciks_by_ticker.values())]
        keep = set(sub["ACCESSION_NUMBER"])

        tr = read_table(zf, "NONDERIV_TRANS")
        tr = tr[tr["ACCESSION_NUMBER"].isin(keep)
                & (tr["TRANS_CODE"] == config.TRANSACTION_CODE)
                & (tr["TRANS_ACQUIRED_DISP_CD"] == "A")]
        own = read_table(zf, "REPORTINGOWNER", ["ACCESSION_NUMBER", "RPTOWNERCIK", "RPTOWNER_TITLE"])
        own = own[own["ACCESSION_NUMBER"].isin(set(tr["ACCESSION_NUMBER"]))]
        notes = read_table(zf, "FOOTNOTES")
        notes = notes[notes["ACCESSION_NUMBER"].isin(set(tr["ACCESSION_NUMBER"]))]

    own["role"] = own["RPTOWNER_TITLE"].map(role_from_title)
    own = own[own["role"].isin(config.ROLES)]

    plan_notes = notes[notes["FOOTNOTE_TXT"].str.contains(RULE_10B5_1_RE)]
    plan_ids = set(zip(plan_notes["ACCESSION_NUMBER"], plan_notes["FOOTNOTE_ID"]))
    fn_cols = [c for c in tr.columns if c.endswith("_FN")]

    def mentions_plan(row) -> int:
        ids = FOOTNOTE_ID_RE.findall(" ".join(row[c] for c in fn_cols))
        return int(any((row["ACCESSION_NUMBER"], i) in plan_ids for i in ids))

    tr = tr.assign(fn_10b5_1=tr.apply(mentions_plan, axis=1) if len(tr) else 0)

    sub_cols = ["ACCESSION_NUMBER", "FILING_DATE", "DOCUMENT_TYPE", "ISSUERCIK", "symbol", "REMARKS"]
    if "AFF10B5ONE" in sub.columns:
        sub_cols.append("AFF10B5ONE")
    df = (tr.merge(sub[sub_cols], on="ACCESSION_NUMBER", how="inner", validate="many_to_one")
            .merge(own, on="ACCESSION_NUMBER", how="inner", validate="many_to_many"))
    flag = df["fn_10b5_1"].astype(bool) | df["REMARKS"].str.contains(RULE_10B5_1_RE)
    if "AFF10B5ONE" in df.columns:
        flag |= df["AFF10B5ONE"].str.strip().str.lower().isin(["1", "true"])
    df["is_10b5_1"] = flag.astype(int)
    return df


def issuer_ciks() -> dict:
    """{v0 ticker: issuer CIK}, from filings in the v0 event window."""
    tickers = set(pd.read_csv(sp500_membership.UNIVERSE_CSV)["ticker"])
    start, end = pd.Timestamp(config.V0_EVENT_START), pd.Timestamp(config.V0_EVENT_END)
    found = {}
    for path in sorted(config.DATA_RAW.glob("*_form345.zip")):
        with zipfile.ZipFile(path) as zf:
            sub = read_table(zf, "SUBMISSION", ["FILING_DATE", "ISSUERCIK", "ISSUERTRADINGSYMBOL"])
        sub["date"] = pd.to_datetime(sub["FILING_DATE"], format=SEC_DATE)
        sub["symbol"] = sub["ISSUERTRADINGSYMBOL"].str.strip().str.upper()
        sub = sub[sub["date"].between(start, end) & sub["symbol"].isin(tickers)]
        for sym, cik in sub.groupby("symbol")["ISSUERCIK"].agg(lambda s: s.mode().iloc[0]).items():
            found.setdefault(sym, int(cik))
    missing = tickers - set(found)
    if missing:
        print(f"WARNING: no filings in the event window for {sorted(missing)}; "
              "their history rows are matched by ticker symbol only.")
    return found


def build() -> pd.DataFrame:
    ciks_by_ticker = issuer_ciks()
    ticker_by_cik = {cik: t for t, cik in ciks_by_ticker.items()}
    zips = sorted(config.DATA_RAW.glob("*_form345.zip"))
    if not zips:
        raise SystemExit("No SEC zips in data/raw/. Run src/fetch_sec.py first.")
    df = pd.concat([load_quarter(p, ciks_by_ticker) for p in zips], ignore_index=True)

    df["filing_date"] = pd.to_datetime(df["FILING_DATE"], format=SEC_DATE)
    df["trans_date"] = pd.to_datetime(df["TRANS_DATE"], format=SEC_DATE)
    df = df[df["filing_date"].between(pd.Timestamp(config.V0_HISTORY_START),
                                      pd.Timestamp(config.V0_EVENT_END))]
    df["ticker"] = df["ISSUERCIK"].map(ticker_by_cik).fillna(df["symbol"])
    df["insider_cik"] = df["RPTOWNERCIK"].astype(int)
    df["shares"] = pd.to_numeric(df["TRANS_SHARES"], errors="coerce")
    df["price"] = pd.to_numeric(df["TRANS_PRICEPERSHARE"], errors="coerce")
    df["usd"] = df["shares"] * df["price"]

    # Same purchase reported in several filings (duplicates, 4/A amendments): keep the earliest.
    before = len(df)
    df = (df.sort_values(["filing_date", "ACCESSION_NUMBER"])
            .drop_duplicates(["ISSUERCIK", "insider_cik", "trans_date", "shares", "price"], keep="first"))
    print(f"dropped {before - len(df)} purchase rows repeated in a later filing or amendment")

    # One insider per filing: CEO before CFO if a joint filing has both.
    df["role_rank"] = df["role"].map({r: i for i, r in enumerate(config.ROLES)})
    first_owner = (df.sort_values("role_rank").groupby("ACCESSION_NUMBER")["insider_cik"].first()
                     .rename("keep_cik"))
    df = df.merge(first_owner, left_on="ACCESSION_NUMBER", right_index=True, validate="many_to_one")
    df = df[df["insider_cik"] == df["keep_cik"]]

    out = (df.groupby("ACCESSION_NUMBER")
             .agg(issuer_cik=("ISSUERCIK", "first"), ticker=("ticker", "first"),
                  insider_cik=("insider_cik", "first"), role=("role", "first"),
                  filing_date=("filing_date", "first"), trans_date=("trans_date", "min"),
                  usd_value=("usd", "sum"), is_10b5_1=("is_10b5_1", "max"))
             .reset_index().rename(columns={"ACCESSION_NUMBER": "accession"}))
    out["usd_value"] = out["usd_value"].round(2)
    out["trade_type"] = "unclassified"
    out = out.sort_values(["filing_date", "accession"])[contracts.TRANSACTIONS_COLUMNS]
    out["filing_date"] = out["filing_date"].dt.date
    out["trans_date"] = out["trans_date"].dt.date
    return out.reset_index(drop=True)


def check_membership(out: pd.DataFrame) -> None:
    """Event rows must be S&P 500 members as of Jan 1 of their filing year."""
    members = pd.read_csv(sp500_membership.MEMBERSHIP_CSV)
    ev = out[pd.to_datetime(out["filing_date"]) >= pd.Timestamp(config.V0_EVENT_START)]
    ev = ev.assign(year=pd.to_datetime(ev["filing_date"]).dt.year)
    joined = ev.merge(members, on=["year", "ticker"], how="left", indicator=True, validate="many_to_one")
    bad = joined[joined["_merge"] == "left_only"]
    assert bad.empty, f"event rows not in that year's S&P 500 list: {bad[['accession', 'ticker']].values}"


def main() -> None:
    out = build()
    assert out["accession"].is_unique, "accession is not unique"
    assert (pd.to_datetime(out["trans_date"]) <= pd.to_datetime(out["filing_date"])).all(), \
        "trans_date after filing_date"
    check_membership(out)
    config.DATA_OUTPUT.mkdir(parents=True, exist_ok=True)
    out.to_csv(config.TRANSACTIONS_CSV, index=False)
    problems = contracts.validate_transactions(config.TRANSACTIONS_CSV)
    if problems:
        raise SystemExit("contract problems:\n  " + "\n  ".join(problems))

    events = out[pd.to_datetime(out["filing_date"]) >= pd.Timestamp(config.V0_EVENT_START)]
    print(f"transactions.csv: {len(out)} purchases ({len(events)} filed in the event window, "
          f"{len(out) - len(events)} history rows); {int(out['is_10b5_1'].sum())} flagged 10b5-1")
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
