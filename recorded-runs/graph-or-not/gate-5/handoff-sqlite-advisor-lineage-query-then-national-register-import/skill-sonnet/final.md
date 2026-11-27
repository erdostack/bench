Still stands: yes

The decision stays `recursive-sql`. The tree page went from 18 ms p95 to 64 ms p95 (staging, full register import). The condition Tomasz and you agreed on, "if the tree page goes past 120 ms p95, look at a graph database properly, and not before", has not been met, and 64 ms is also well inside the graduate school's 250 ms budget.

Old number next to new:
- p95 of the tree page: 18 ms recorded, 64 ms now. That is 64 / 120 = about 53% of the agreed trigger, and 64 / 250 = about 26% of the budget. Headroom to the budget fell from about 14 times (250 / 18) to about 3.9 times (250 / 64).
- Researchers: 41,000 recorded, 390,000 now (about 9.5 times).
- Advising rows: 46,500 recorded, 452,000 now (about 9.7 times). Rows per researcher are 452,000 / 390,000 = about 1.16, against 1.13 before, so fan-out has not grown.
- Deepest lineage: 19 recorded, 27 now.

Data grew about 9.5 times and latency about 3.6 times (64 / 18), so the query is scaling well. The graph-database rung needs SQL measured failing at the required depth, and that has not happened.

One thing to watch: the deepest lineage is 27 generations and `sql/ancestors.sql` stops at 30. That leaves 3 generations of room. A lineage deeper than 30 would be cut off without any error. Nothing needs to change today, but someone should check whether the 27 is real depth or a data-entry loop that the path guard is already catching.

What I did not check: the 64 ms is your staging figure. I could not re-measure it, because there is no database copy in the repo. I also don't know whether it includes the deepest lineages. I have no query plan either. Both were unknown before this import and still are.

Because the decision stands, I did not change `docs/graph/DECISION.md` or anything else in the repo. If you want the staging numbers on record, I can add them next to the old ones. I would also take the same p95 measurement on production data after go-live. The 120 ms trigger from the record still applies.
