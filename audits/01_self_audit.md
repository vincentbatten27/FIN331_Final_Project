Audit of checkpoint 2
Part 1 


Issue 1: 

By far the most presing issue is the fact we only have 1 working sample. This is due to the fact that we ran a limited 
sample, both in years and companies. We ran only 10 firms, and used only 6 months. If we expand this to many years, and
all 500 companies, we assume it is self evident that we will find more results to use. In that period, there were
7 events, with only one being marked opportunistic, WY's CFO. That being said, the event was a purchase, and the shares 
fell ~11% following, so it is not a very evidence based on the directionality of the event (t-statistic of -1.4). 

Issue 2: 

Secondly, we found it hard to find a free list of S&P 500 memebrship data. Luckily, we had a prior list handy of yearly 
memebrship data for other project work. One caveat, though, is this is yearly, not quarterly as S&P 500 reblancing is.
Becuase of this, their is surviviroship bias, as firms may be removed or added mid way through the year, excluding them 
from our study, but are still marked as valid. We are attempting to recitfiy this down the road by having a wikipedia 
scraper mark the exact entrance and exit date, but their is rough draft, we saw it as a valid solution. 

Part 2


Fix 1: 

Why have not addrssed this fully yet, as we saw it as a postive sign for the flaggin/marking logic to hold. We also dont 
see it as an 'issue' sp to speak, as we beleive more data will curve the conecern.

Fix 2:

This one has been marked and proposed, but given the limtied 6 month window, not tested. First thing on the next itteraiton
will be ensuring the Wikipedia scraper and marker work properly to mark entrance/exit of S&P 500 to ensure we are abding
by our rulset.

Part 3
Reproduces: not yet (clean-clone rebuild untested)
Provenance: OK (DATA_SOURCES.md)
Unit of observation: OK (accession is unique, asserted)
No look-ahead: OK for the event date and classifier; problem for membership (Jan-1 snapshots)
LLM leakage: OK / not applicable (no LLM in the pipeline), but LLM being utizlied in work could have some influence here.
p-hacking: OK so far (specs_tried.md), but only a few specs so far
Magnitudes: not yet (one event)
Hand checks: OK for the event study (built-in recompute); not yet for transactions and the classifier on EDGAR
Honest limits: OK (threats section)
You understand it: OK


