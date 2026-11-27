Decision: recursive-sql

The shutdown check is a reachability question, not a lookup, so it is a graph problem. But it is a very small one: 640 stations and 1,500 one-way segments (your numbers), checked about 30 times a day, with the layout changing a few times a year. One recursive query on the SQLite layout file you already run does it. I did not need Neo4j, and I did not need networkx.

What it turns on:
- Work per check is at most 640 stations and 1,500 segments. I timed a recursive query on a synthetic graph of that size (SQLite 3.53.1, in memory, with an index on segment.to_station) at about 1.4 ms per check, averaged over all 640 stations. That is synthetic data, not your real layout. var/layout.db is git-ignored and was not in the repo.
- 30 checks a day with no stated latency budget is far below anything that needs a second system. Neo4j would add a server, a feed from the SQLite file that can drift, and a new query language, all for 1,500 edges.
- networkx is pinned in requirements.txt but nothing imports it. It would also work at this size. I chose SQL because it needs no loader and no second copy of the layout to keep fresh.

How to build it (I changed nothing in the code; the only file I added is docs/graph/DECISION.md):
- The rule is a walk backwards from the docks along belt and roller segments only, in their direction, with the station being taken out removed. A station is cut off if it could reach a dock before and cannot after. Stations that are already cut off today should not be blamed on this shutdown.
- The existing linewatch/reach.py does not do this. It follows segments in both directions, includes bypass segments, walks outward from the station and not toward a dock, and runs one query per station. Rewrite it as one recursive query, and add an index on segment(to_station) to db/schema.sql.

What I could not find or measure: the real layout file (dock count, real fan-out, cycles, stations already cut off), any latency budget, and whether this runs in a request or as a report. If the real file shows a check slower than the budget maintenance sets, move to networkx. If the plant grows by orders of magnitude, revisit a graph database.
