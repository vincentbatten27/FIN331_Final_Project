# STATUS: Checkpoint 1 memo

_To be written by hand by the team (about 3 paragraphs). Keep it: it shows where
the project started._

1. **What we picked and why.**
   We selected seed 8, 'Following the Insiders'. The idea is to see whether information can be gained from  insiders purchasing behavior, and observing whether opportunistic insiders (no patterns) can flag trading opportunities. One example is say, observing a CEOs trading behavior, and when that CEO sells off a number of their shares, is it indicative to a leading indicator of negative news about the company. We picked this for one out of personal interest from the three of us, and secondly due to the relation to the event study work we did in class. 
3. **What our proof of concept got, and what broke.**
   Our proof of concept is a repo skeleton with schemas for the events panel and transactions CSVs. A validator script was made as well that checks the CSV, the sample rows, and the Streamlit app that runs the sample data (essentially a substitute for cross referencing the many files, agents choice for efficiency). One hiccup was the need of yearly SP500 constituents, but a team member had a CSV of that exact information handy on their computer (lovely coincidence). Nothing has broke yet, but their has been no full sample runs of abnormal returns, nor has their been any SEC data downloaded yet. 
5. **Our questions for the instructor.**
   Nothing pressing at the moment. After checkpoint 2 is complete and we have a full walk through, we likely will have a better idea of the feasibility of certain parts and possible issues, so we will reserve questions for then. 
