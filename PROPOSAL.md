# Do CEO and CFO Purchases Predict Returns?

**Team:** WACC Warriors

**Members:** Vincent Batten, Eric Schneps, David Kyle

**Live dashboard:** https://fin331-finalproject.streamlit.app/

---

## 1. The question

**When the CEO or CFO of an S&P 500 company buys their own stock, does the stock beat the market over the next month, and is that signal stronger when the purchase deviates from the insider's regular practices?**

Executives, competent ones at least, should know more about their companies than do investors. Therefore, when they spend their own money buying their stock, in theory, they are the most informed investor. And being the most informed means their trades should be making profit. However, many insider purchases are simply routine. Some executives make purchases after bonuses, or every year on a certain date. These transactions do not interest us because they are not placed on the idea that the stock is undervalued. Our team wants to distinguish between these "routine" traders and "opportunistic" ones, meaning insiders whose purchases are not routine. And we would like to see if opportunistic purchases can actually predict abnormal returns. We can achieve this goal using a fresh sample of large-cap companies constructed from publicly available data.

**Who would pay for this?** A stock screener would be the best fit. Platforms for retail traders already display insider buying as a simple raw feed like "CEO bought $250k of _____". But these feeds cannot distinguish "routine" from "opportunistic" purchases. And it is a more valuable product than that because a screener displaying only the latter along with historical performance of such trades can help a subscriber to act the very same day.

---

## 2. The data

### Unit of observation

Each row represents an open-market purchase made by a CEO or CFO of a single firm from a Form 4 filing. We dated the event according to the day when the filing becomes available at the SEC since this is the first day an outside investor could have learned of the trade. Rows below represent an output of our first end-to-end run for 10 randomly chosen S&P 500 companies.

| accession | ticker | role | filing_date | trans_date | usd_value | is_10b5_1 | trade_type | car_1_20 |
|---|---|---|---|---|---|---|---|---|
| 0001214659-18-006671 | LKQ | CEO | 2018-10-29 | 2018-10-26 | 53,100 | 0 | unclassified | (history) |
| 0001225208-19-004964 | NOC | CEO | 2019-03-08 | 2017-10-16 | 19,770 | 0 | unclassified | (history) |
| 0001225208-20-008449 | UPS | CEO | 2020-06-02 | 2020-05-29 | 1,003,233 | 0 | unclassified | (history) |
| 0001209191-21-030636 | WY | CFO | 2021-05-06 | 2021-05-05 | 385,600 | 0 | unclassified | −0.1065 |

"trade_type" is routine, opportunistic or unclassified if the insider lacks sufficient history. "car_1_20" is a measure of how well the stock performed compared to its expected return over the next 20 trading days after the filing. Older rows are used for classification purposes only. The NOC purchase happened in October 2017 but wasn't reported until March 2019, so we would use a wrong date if we would date it by the trade since we would be relying on information not available to the public for 17 months.

### Sample

We use filings from 2020 through 2022 as well as older filings from 2017 needed for classification. A firm is considered included if it belonged to the S&P 500 on the filing date. We consider only open-market purchases of at least $10,000. Purchases under 10b5-1 plans are flagged and excluded from the results.

In addition to the event date and insiders' ID and role, the variables used in our analysis are the amount of the purchase, the flag for 10b5-1 purchases, daily stock price and SPY, and S&P 500 membership status by date. If we have time, we might also include insider sales, Fama-French factors, and purchases by other officers and directors.

### Raw inputs

Three public data sources are used in this research. The insider transactions are pulled from SEC's quarterly Insider Transactions Data Sets, saved to "data/raw/" via "src/fetch_sec.py". Stock and SPY daily prices are downloaded using the "yfinance" package via Yahoo Finance and saved by "src/fetch_prices.py" to "data/raw/prices/". The list of S&P 500 members starts from the members as of January 1st of each year, kept in "data/reference/", and will be filled in with mid-year changes from Wikipedia, which "src/sp500_membership.py" does. Download dates of each file are recorded in "DATA_SOURCES.md".

---

## 3. Method

### Pipeline

"python run_all.py" runs these steps in order:

1. "src/sp500_membership.py" constructs the list of S&P 500 members by date.
2. "src/fetch_sec.py" downloads the SEC insider transactions files.
3. "src/build_transactions.py" keeps only CEO/CFO purchases, eliminates duplicate filings, and marks 10b5-1 transactions.
4. "src/fetch_prices.py" downloads the daily prices.
5. "src/event_study.py" computes abnormal returns after every filing.
6. "src/classify_insiders.py" marks every transaction as either routine or opportunistic.
7. "src/data_description.py" and "src/report.py" generate tables and charts and save them into "outputs/".
8. "app.py" is the application dashboard.

### Insider transaction classification

Each purchase is compared to the insider's trades in the previous three years, but only to the ones that had already been filed. If the insider traded in the same month during each of those years, the purchase is classified as routine. If they traded, but not consistently in the same month, it is opportunistic. If the insider doesn't have sufficient history, we classify the trade as unclassified.

### The event study

We fit a market model using SPY returns from about one year prior to each filing, and it gives an expected stock return for each day after the filing. The abnormal return is the actual minus the expected return, from days +1 to +20 relative to the event (filing). Day 0 is not counted because a filing can come out after the market closes, so an investor who read it might not be able to trade until the next day.

### The analysis

1. Compute the average 20-day abnormal return for both categories of purchases and test whether each is different from zero. Then find out whether opportunistic purchases earn a significantly higher abnormal return than routine purchases.
2. Repeat with another benchmark, with 10b5-1 transactions included, and with only large purchases.
3. Additionally, we could run the same test on insider sales. We should expect a weaker result there, since executives often sell for personal reasons like taxes.

An event study fits this question because each filing is a specific day when new information reaches the market.

---

## 4. Threats and mitigations

The most significant threat that was apparent to us in this study is look-ahead bias. If we used the trade date, we would have been using information nobody knew yet (like the NOC row, for example), so we will use the event date (the filing date). The same problem could show up when classifying trades if we used filings the insider made later, so the classifier only looks at filings from before each purchase.

The next threat we have to consider is survivorship. Today's S&P 500 list leaves out the stocks that were dropped from the index, so we base it upon the membership as of each filing date. Duplicate and amended filings can make one and the same trade appear in two or more filings, so we are keeping only the earliest filing.

In order to prevent ourselves from p-hacking, all of the settings are fixed in "src/config.py" prior to looking through any results, and each new attempt gets recorded in "specs_tried.md".

Finally, a more practical threat for this project is sample size. Big companies' executives do not often purchase stock in their own company, and our first run found only one usable event across 10 firms in six months. We are hoping that using the whole S&P 500 for three years will make a difference, but if there is still a lack of routine transactions to compare with, other officer transactions will be included.

---

## 5. Dashboard mockup

![Dashboard home page](docs/images/dashboard_screenshot.png)

The home page shows the latest opportunistic purchases, with how similar trades have done in the past next to each one. The other tabs cover the method and results and let you search through all the trades. There's already a working version with placeholder data at the link up top.
