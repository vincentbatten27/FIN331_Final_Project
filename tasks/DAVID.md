# Brief for David (Product manager), branch `David`

**Goal:** a live four-page Streamlit dashboard (intro, methodology, results, explore) that reads from `outputs/` (and falls back to `data/sample/` until real files exist), deployed on Streamlit Community Cloud, with its link at the top of `README.md`.

**Read first:** `CLAUDE.md` (hard rules), `README.md` (schemas, `outputs/` file names), and the docstring at the top of each page stub.

## Files you own (edit only these)
`app.py`, `pages/1_Intro.py`, `pages/2_Methodology.py`, `pages/3_Results.py`, `pages/4_Explore.py`, `docs/images/` (mockup).

## Sample outputs already exist (use them now)
`outputs/sample/` holds `summary_by_trade_type.csv`, `car_by_trade_type.png` and `data_description.csv`, built from the fake sample rows. Real results will appear in `outputs/` with the same file names. Each page should read `outputs/<file>` if it exists, otherwise `outputs/sample/<file>` with a visible "SAMPLE DATA" warning.

## You do NOT have to wait for anyone
The data scripts are being built in parallel. Build against `data/sample/` (fake rows with the same columns). When real files land in `outputs/` and `data/output/`, the same code reads them.

## Do in this order (each step has a "done when")
1. **Mockup first.** Sketch the finished dashboard (Excalidraw works; a photo of a drawing is fine). Save it as `docs/images/dashboard_mockup.png`. Done when the file is committed.
2. **`pages/4_Explore.py`.** Move the filter table now in `app.py` here. Done when you can filter by trade type and role and see CAR.
3. **`pages/3_Results.py`.** Show `outputs/summary_by_trade_type.csv` and `outputs/car_by_trade_type.png` if they exist; otherwise show the sample with a visible "SAMPLE DATA" warning. Done when the page works with and without those files.
4. **`pages/1_Intro.py` and `pages/2_Methodology.py`.** Plain text: the question, who would pay, data sources, pipeline steps, threats. Read parameters from `src/config.py`; do not retype numbers. Done when both pages load.
5. **`app.py`.** Make it the landing page that links to the four pages.
6. **Deploy** on Streamlit Community Cloud from branch `checkpoint-2` (or `David`), main file `app.py`. Done when the URL loads. Put the link at the top of `README.md`.

## Check before every PR
- `streamlit run app.py` starts and every page loads with no errors.
- No file downloads, no model fitting, no hard-coded numbers inside the app. Every number shown comes from a file.

## Do not
Edit `src/` scripts, `src/config.py`, or the schemas; or push to `main`.

## When done
Commit, push branch `David`, and open a pull request into `checkpoint-2`. Tag Vincent.
