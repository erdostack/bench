Decision: need-more-information

The depth is the missing fact, and the two numbers on the table lead to different options. Nothing was run or measured, and nothing in the repo was changed except the new `docs/graph/DECISION.md`.

What it turns on:
- At 2 steps (the PM), the walk reaches about 16.8^2 = 283 members on average (6.4M follow rows / 380,000 members = 16.8 per member), and your existing indexes in both directions serve it. That points to recursive-sql on the SQLite file you already run, to be timed against the 150 ms budget at 70 views a second before it ships. Neo4j would not be needed.
- At up to 6 steps (Dana), the average reach is 16.8^6, about 22 million, more than the 380,000 members, so most of the network is in range. This needs measuring: a walk from both sides (3 steps each, about 4,700 rows per side on average) on the real follow data, including hubs. Within 150 ms it stays recursive-sql; over it, it is an in-process library if 6.4M edges fit in the memory of one app-server process and can be reloaded often enough, otherwise a graph database.

Questions for the meeting and after:
1. How many steps must the badge reach? The PM and Dana decide this. If 2, the answer is recursive-sql; if 6, run the measurement above.
2. Does a step follow the arrow only (you follow someone who follows them) or either way? The TODO does not say. Either way roughly doubles the edges walked.
3. What does the badge show when nothing is found within the depth, and how stale may it be?
4. How fast do follows change, how many app-server processes run, and how much memory does each have? These size any in-memory copy.

I could not find: the tail fan-out (hubs), any timing on the real data (no database file is in the repo), or the follow write rate.
