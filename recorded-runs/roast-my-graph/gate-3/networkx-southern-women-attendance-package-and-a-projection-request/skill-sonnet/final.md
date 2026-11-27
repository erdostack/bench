No, the TA is not right, and you should keep the event nodes. I'd change nothing before class.

The projection to woman-to-woman keeps only one number per pair of women (how many events they shared). Three of your four class questions need the events themselves. Question 1 (big gatherings) needs how many women went to each event, for example E8 with 14. Question 3 (events bridging the two groups) needs to know which events each woman attended, and your answer is E6, E7, E8 and E9. Question 4 (events two given women both attended) needs the event names, and for Evelyn Jefferson and Nora Fayette the answer is E6 and E9. A projection can't produce any of those. Only question 2, the two groups, uses the projection, and `co_attendance` already builds it from the full graph on demand, so nothing can drift out of step. The events also aren't a join table in the "just two sides" sense, because the class asks questions about them directly.

I ran `python -m events.analysis` and the answers are correct. Modularity gives exactly two groups of 10 and 8 women, which is what question 2 expects.

I found no problems in the files, so `findings.json` is an empty list (`[]`). The full write-up is in `docs/graph/ROAST.md`. I did not edit any code.
