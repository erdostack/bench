# Graph decision

Decision: recursive-sql

The question was how to count the families a family can reach through one, two and three marriages for the seminar's reach panel, and whether that needs Neo4j, the networkx we already have, recursive SQL on the SQLite file, or no graph. It is a walk of fixed depth (3) over 16 families and 20 ties, so a recursive query on the existing SQLite file already answers it: in a measurement it matched networkx for all 16 families and ran in about 1.4 ms in total. Neo4j would be a second system for static data of 20 rows.

## Workload facts

- Question asked of the connections: families reachable from one family within 1, 2 and 3 marriage ties, a walk along a relation between things of the same kind for a fixed depth of 3 (request; TODO in seminar/app.py; marriage_tie in db/schema.sql).
- Stated by the user: the data is Padgett and Ansell's Florentine families, 16 families including the Pucci, and 20 marriage ties.
- Stated by the user: the data never changes.
- Stated by the user: the seminar has 25 students using it for a term.
- Stated by the user: a colleague wants Neo4j "to do it properly" so students learn a real graph database.
- Measured (python3, sqlite3 3.53.1, networkx 3.7, in-memory database built as seminar/load.py builds it, nothing written to the repo): 16 families and 20 marriage_tie rows, matching the stated numbers.
- Measured: a recursive query over both directions of each tie, depth capped at 3, `min(d)` per family, gave per-distance counts equal to `nx.single_source_shortest_path_length(g, f, cutoff=3)` for all 16 families, 0 mismatches. The 16 queries together took about 1.4 ms.
- Measured: Medici reach 6 families at one marriage, 5 more at two, 3 more at three; Pucci have no ties, so reach nothing at any depth (same run). Counts are exact distances; add them up if the panel should show "within N".
- Fan-out: 2 x 20 / 16 = 2.5 ties per family on average (sum from the stated numbers); the tail is unknown here and is irrelevant at this size.
- Writes and freshness: none; the data never changes (stated by the user), and `var/seminar.db` is rebuilt by `python -m seminar.load` (README.md).
- Load: 25 students for one term, so the lookups are few, on 16 rows (stated by the user).
- What is operated today: Flask and SQLite (`var/seminar.db`); networkx 3.7 is in requirements.txt and used by seminar/load.py only (seminar/app.py reads SQLite directly).
- unknown: the number of lookups per day; nothing in the repo records usage and no latency budget is stated. At 1.4 ms for all 16 families this does not decide anything.

## Options considered

- graph-database (Neo4j, as the colleague proposes): rejected, because 20 ties that never change, with 25 users, do not need a second stateful store, a load step and a new query language. Learning Neo4j is a teaching goal, not a need of this workload; treat it as a separate exercise if the seminar wants one.
- in-process-library (networkx, already a dependency): rejected only because a cheaper rung holds; it would also work (16 nodes in memory). Use it if the team prefers to keep the walk in Python, since app.py would need to import it and build the graph at start-up.
- recursive-sql (recursive query on the existing SQLite file): chosen, because it was measured equal to networkx on all 16 families and takes about 1.4 ms for all of them. Use `UNION` rather than `UNION ALL` so each family is visited once, add both directions of each tie, cap the depth at 3, and take the minimum distance per family. Pucci come out with no rows, so show 0, 0, 0.
- no-graph (plain joins, no traversal): rejected, because the question follows the marriage relation between families up to three times; two- and three-step walks are a chain of self-joins, which the recursive query already is.

## What would change the decision

- The requirement growing to a deeper or data-dependent depth, or to a data set with thousands of families that changes continuously, would be tested against the recursive query first, and move this to in-process-library or graph-database only if a measurement on the larger data fails; the seminar owner sets the latency limit, as none is stated.
- The seminar choosing "learn Neo4j" as a teaching goal would justify Neo4j as a separate exercise, not as the engine of this panel.
