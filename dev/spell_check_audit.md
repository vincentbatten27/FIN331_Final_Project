# Spell check audit (Checkpoint 3)

Date: 2026-11-17 · By: Eric · Scope: every tracked `.md` file and the comments and strings in every tracked `.py` file.

**Method:** `pyspellchecker` (English dictionary) flagged about 70 unknown words, and each was reviewed by hand. Most are project jargon and are correct (yfinance, Pomorski, survivorship, dedupe, streamlit, lookback, noqa). A dictionary check can't catch a real word used wrongly ("their" for "there"), so those below were found by reading the flagged lines.

**Result:** 23 errors, all in two hand-written files owned by Vincent (README "Not agent work"). None in the code or in the other docs. Per CLAUDE.md rule 7 these are listed for the owner to fix, not edited here. `audits/01_self_audit.md` is also the version the instructor audited, so whether to change it is the owner's call.

## `audits/01_self_audit.md`

| Line | Written | Should be |
|---|---|---|
| 7 | presing | pressing |
| 15 | memebrship | membership |
| 16 | memebrship | membership |
| 16 | reblancing | rebalancing |
| 17 | Becuase | Because |
| 17 | their is | there is |
| 17 | surviviroship | survivorship |
| 17 | mid way | midway |
| 18 | recitfiy | rectify |
| 26 | Why have not addrssed | We have not addressed |
| 26 | postive | positive |
| 26 | flaggin | flagging |
| 26 | dont | don't |
| 27 | sp to speak | so to speak |
| 27 | beleive | believe |
| 27 | conecern | concern |
| 31 | limtied | limited |
| 31 | itteraiton | iteration |
| 32 | abding | abiding |
| 33 | rulset | ruleset |
| 40 | utizlied | utilized |

## `PROPOSAL.md`

| Line | Written | Should be |
|---|---|---|
| 17 | equiter researcher | equity researcher |
| 77 | analsyis | analysis |

## Grammar noticed in passing (`STATUS.md`, Checkpoint 1 memo)

| Line | Written | Should be |
|---|---|---|
| 9 | their has been no full sample runs | there have been no full sample runs |
| 9 | Nothing has broke yet | Nothing has broken yet |

The README says to keep `STATUS.md` as a record of where the project started, so these may be best left as they are.
