Decision: recursive-sql

Not Neo4j. Counting introductions between two members is a shortest-path walk, so it is a graph question, but at under 200 members and about 50 lookups a day it fits in the SQLite file you already run.

What I measured (in memory, nothing written to the repo):
- I rebuilt the demo club (34 members, 78 ties, 231 encounter rows). A recursive query over ties with at least 3 contexts agreed with networkx on all 1,156 member pairs. It took about 0.3 ms per lookup.
- On a synthetic 200-member club (591 ties, denser than the demo), the same query averaged about 7.6 ms and took 38.6 ms at the slowest. That club is made up, not platform data.
- The welfare rule (at least 3 contexts) drops 30 of the 78 demo ties (48 stay). It also leaves 6 members with no qualifying tie, so 366 of 1,156 pairs have no path. The panel needs a "no introduction path" answer.

How to build it: take the ties with `GROUP BY member_a, member_b HAVING COUNT(*) >= 3`, add both directions of each tie, and walk with `UNION` (not `UNION ALL`) and a depth cap. club/graph.py counts every encounter row with no threshold, so do not reuse it as it stands. Staying on networkx with the same filter is a fine fallback.

Not found: how often encounters are written, how fresh the panel must be, and the real platform's tie counts. The repo has only the demo data.

I wrote docs/graph/DECISION.md and changed nothing else.
