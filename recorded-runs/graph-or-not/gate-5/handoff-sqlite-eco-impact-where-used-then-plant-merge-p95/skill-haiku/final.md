Still stands: no

The call we made was recursive-sql: keep the upward BOM walk on the Postgres replica while the impact screen's p95 stays under 800 ms. The Ostrava merge broke that condition. The p95 is now 1.3 s, over the agreed limit, so the rule that Ines and you agreed last spring moves the walk into the ECO service's memory with networkx. I have updated docs/graph/DECISION.md to say so and kept the old values beside the new.

Numbers, old then new:
- BOM lines: 400,000 then 1,100,000 (2.75 times).
- Impact screen p95: 180 ms then 1.3 s (7.2 times). Limit 800 ms, so the screen is now 1.6 times over it, where before it had 4.4 times headroom.
- Load: about 600 screens a day, not restated. At the stated p95 for every call that would be about 780 s of query time a day, against 108 s before.

Why networkx and not the other options:
- A graph database is still not needed. 1.1M BOM lines fit in one process: Ana's prototype held the earlier data in 350 MB and answered in 20 ms. If it was built on the old 400,000 lines, linear scaling gives about 960 MB at the new size. That is an extrapolation.
- The recursive query is not the fix yet. Its measured p95 is over the limit, and the rewrite that removes repeated route rows has not been run, so it does not reopen that option.

Before you commit to the move, I need three things:
1. The window and method behind the 1.3 s p95. If it is a spike or a cold-cache run, the answer could come back to recursive-sql, and the rewrite would have to be run first.
2. The item count after the merge, and how many ECO service processes would each hold a copy.
3. How often PLM imports change the BOM, and how stale the screen may be. That decides whether a reload meets the freshness the readers need.

The first step is to load the full 1.1M-line BOM into one ECO service process and measure memory, load time and a few walks. networkx is already pinned in requirements.txt (3.7) but nothing in the repo imports it.

Nothing else in the repo was changed. The only file edited is docs/graph/DECISION.md.
