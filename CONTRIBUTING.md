# Contributing: team setup and prompts

How the three of us work in this repo. (Moved out of the README so the README can describe the project.)

**Your job is in your brief:** [Eric](tasks/ERIC.md) · [David](tasks/DAVID.md) · [Vincent](tasks/VINCENT.md). Your coding agent reads it for you.

**New to GitHub? The idea in one minute.** The repo is a shared folder. A *branch* is your own private copy of it, so you can work without breaking the shared one. A *pull request* is you saying "I'm done, please add my work." Your agent does the Git commands for you.

## Setup (once)
1. Accept the GitHub invite in your email.
2. Install GitHub Desktop and VS Code. In GitHub Desktop choose File → Clone repository → `FIN331_Final_Project`. Open the folder in VS Code and start your coding agent there.
3. Paste **Prompt A** (below), replacing `<NAME>` with `Eric`, `David` or `Vincent` (same for Prompt C).
4. Then paste **Prompt C**: "Read `CLAUDE.md` and `tasks/<NAME>.md`. Do the steps in order, one at a time. After each step, check its 'done when' line and show me the result before starting the next. Edit only the files my brief says I own."
5. When finished, paste **Prompt B**.

**Prompt A (setup):**
> Read `CLAUDE.md` and `README.md`. I'm new to GitHub, so explain each step in one short sentence. Please: (1) switch to the current integration branch (`checkpoint-2` for Checkpoint 2, `checkpoint-3` for Checkpoint 3); (2) create my own branch called `<NAME>` from it, replacing any older local copy; (3) create a `.venv` and install `requirements.txt`; (4) copy `.env.example` to `.env` and tell me exactly what to type for `SEC_USER_AGENT` (do not fill it in yourself). Never touch `main`. Stop when done and tell me what you did.

**Prompt B (send it back):**
> Show me every file that changed. If they are all files I own (listed in my brief), commit them with a clear message, push my branch, and open a pull request into the integration branch (not `main`). Then give me the link.

## Facts everyone needs
- **v0 scope (in `src/config.py`):** 10 tickers drawn with seed 331 from the Jan-1-2021 S&P 500 list in `data/reference/`, events filed 2021-01-01 to 2021-06-30, history from 2018-01-01.
- **`outputs/` files the app reads:** `data_description.csv`, `summary_by_trade_type.csv`, `car_by_trade_type.png`.
- **Nobody waits on anyone.** The app and the Analyst scripts build against `data/sample/` until the real files land.
- **Stub files** (`src/*.py`, `pages/*.py`) have instructions in their docstrings. Fill them in; do not rename them.
- Check before any PR: `python run_all.py --sample` prints `sample contracts: OK`.

## Not agent work (written by hand, Vincent)
`STATUS.md` memo, `audits/` write-ups, `PROPOSAL.md`.
