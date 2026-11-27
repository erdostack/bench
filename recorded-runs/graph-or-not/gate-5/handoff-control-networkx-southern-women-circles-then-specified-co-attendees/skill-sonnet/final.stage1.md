Decision: in-process-library

The circles page is a real walk: from one woman, to the women she shared events with, then to theirs, out to the whole network, and the depth depends on the data. So it is not a no-graph problem. But the data is tiny and fixed, and it does not need Neo4j.

What it turns on:
- I counted data/attendance.csv: 89 attendances, 18 women, 14 events. That matches your numbers. From every woman, all 18 women are reachable, and the furthest any two women are apart is 2 steps (from Brenda Rogers: 1 woman at step 0, 15 at step 1, 2 at step 2).
- 89 edges that never change, read by a few dozen visitors a week, fit in memory many times over. Even at a generous 1 KB per edge that is about 89 KB, and there is no freshness question because the data never changes.
- There is no SQL database in the repo, only the CSV, so recursive SQL has nothing to run on. networkx 3.7 is already pinned in requirements.txt, so load the CSV once with the existing load_attendance() and walk it. A short plain-Python breadth-first loop would also do.
- Neo4j would add a server to deploy and keep running on a small shared host, for 89 rows. "It's a social network" describes the picture, not the workload.

I changed no code; the only file I added is docs/graph/DECISION.md.

What I could not find: the shared host's memory limit and whether it can install networkx (the README assumes it can). Neither would change the answer at this size. It would change if the data grew to hundreds of thousands of rows or started changing continuously.
