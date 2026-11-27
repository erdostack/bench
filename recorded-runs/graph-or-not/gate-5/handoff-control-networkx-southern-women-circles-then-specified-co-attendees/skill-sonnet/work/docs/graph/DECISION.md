# Graph decision

Decision: in-process-library

The question was how to build the "circles" page (pick a woman, show who she is connected to through shared events, then who they are connected to, step by step out to the whole network) and whether that needs Neo4j, as a board member suggests. It is a real walk of data-dependent depth, but the data is 89 attendance rows that never change and live in a CSV file, so there is no SQL database to recurse in; loading them into memory with networkx 3.7, already pinned in requirements.txt, is the cheapest option that holds.

## Workload facts

- The question asked of the connections: from one woman, who shared an event with her (step 1), then who shared an event with those women (step 2), and so on out to the whole network, which is a walk through the woman-event-woman relation to a depth the data decides (stated by the user; society/pages.py TODO).
- 18 women, 14 events, 89 attendances, and the data will never change (stated by the user). Counted: data/attendance.csv has 89 rows, 18 distinct women, 14 distinct events (measured: counting with Python over the CSV).
- Depth, measured: every woman reaches all 18 women, and the greatest number of steps between any two women is 2 (measured with a breadth-first walk over data/attendance.csv, women linked when they share an event). For the first woman in the file, Brenda Rogers, the steps are 1 woman at step 0, 15 at step 1, 2 at step 2.
- Load: a few dozen visitors a week on the society's small shared web host (stated by the user), so well under one request an hour; no latency budget is stated, none is plausibly at risk.
- Storage: the data is `data/attendance.csv`, read by `load_attendance()` in society/data.py; `setup.py` generates it from the copy bundled with networkx (README.md). There is no database in the repo and none is mentioned, so there is no SQL engine to run recursive queries in.
- networkx==3.7 is pinned in requirements.txt and the README tells the reader to `pip install -r requirements.txt` (requirements.txt, README.md). It is not yet imported in society/.
- Edges, derived: 89 attendance edges (given by the CSV row count); even as a woman-to-woman graph, at most 18 x 17 / 2 = 153 pairs.
- Memory, derived: 89 edges x even 1 KB per edge (a deliberately generous figure, not measured) = about 89 KB, trivial for one process, and the data never changes, so no reload or freshness question arises.
- unknown: the shared host's memory limit and whether it can install networkx (the README already assumes it can); looked in README.md, requirements.txt, society/. Neither would flip this decision at 89 edges.

## Options considered

- graph-database (Neo4j, as the board member suggests): rejected, because 89 edges that never change, read a few dozen times a week on a small shared host, are nowhere near the profile that justifies a server to deploy, back up and run. "It's a social network" describes the picture, not the workload.
- in-process-library (loading the CSV into memory and walking it with networkx 3.7): chosen, because the edge set is 89 rows (about 89 KB at a generous 1 KB per edge), it never changes so freshness does not matter, the CSV is already read by the app, and networkx is already a pinned dependency. A plain breadth-first loop over dictionaries from the same CSV would also do, and needs no library at all. This is a proposed approach; no code was changed here.
- recursive-sql (recursive queries on an existing SQL database): rejected, because there is no SQL database in the repo to run them on (data is a CSV file, society/data.py); adopting one just for 89 rows would add a second copy of the data and a load step for no gain.
- no-graph (plain joins, no traversal): rejected, because "who they were connected to, then who they were connected to, step by step out to the whole network" follows the woman-to-woman relation through shared events for more than one step.

## What would change the decision

- The data growing from 89 attendances to hundreds of thousands, or being updated continuously with visitors needing fresh answers, would move this to recursive-sql (if the data then lives in a SQL database) or to graph-database (only if SQL were measured failing at the needed depth).
- The society moving the attendance list into a SQL database that the site already operates would make recursive-sql an equal choice; this is the cheaper rung and would then win.
- The shared host being unable to install networkx would move this to a short plain-Python breadth-first walk over the CSV, not to another option.
