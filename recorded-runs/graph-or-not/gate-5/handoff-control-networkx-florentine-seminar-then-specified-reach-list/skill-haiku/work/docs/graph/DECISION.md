# Graph decision

Decision: recursive-sql

The seminar asks how many other families each family can reach through one, two and three marriages, and the colleague proposes Neo4j for teaching. The walk is short and fixed at three steps over 16 families and 20 marriage ties (stated by the user), a size where the SQLite file the app already reads answers the question with a recursive query, so Neo4j is not needed for the panel. The finding it turns on is the depth: a three-step walk over 16 nodes, which the recursive query returned the same counts as networkx for every family, all 16 checked.

## Workload facts

- The question asked of the connections is the number of distinct other families reachable from a family within 1, 2 and 3 marriage ties: a short walk of fixed depth 3 from a starting point (stated by the user; `seminar/app.py` TODO: "reach" panel for the family pages; no query runs yet).
- Families: 16, including the Pucci (stated by the user; `seminar/load.py` inserts the 15 networkx families plus Pucci; `db/schema.sql` `family` table).
- Marriage ties: 20 (stated by the user; `db/schema.sql` `marriage_tie`, one row per pair; `seminar/load.py` inserts `g.edges()` of `florentine_families_graph`).
- Measured on the bundled networkx graph (`florentine_families_graph`, networkx 3.7, Python 3.13.18): 15 nodes, 20 edges; the Pucci has no ties (`README.md`), so its reach is 0 at every depth.
- Depth: fixed, 3 steps (stated by the user). Depth needed is not larger because the panel asks for 1, 2 and 3 only.
- Fan-out: 2 x 20 / 16 = 2.5 ties per family on average (arithmetic from the stated counts). The per-family tail was not measured separately.
- Size of required work: at most 16 families times 20 ties per depth step, so under 16 x 20 = 320 row checks per step (arithmetic bound; not timed).
- Load: 25 students for a term (stated by the user); one page view per family, a small number of calls, no latency budget stated.
- Writes and freshness: the data never changes (stated by the user); the database is rebuilt by `python -m seminar.load` (`README.md`), so no freshness requirement applies.
- What is operated today: SQLite file `var/seminar.db`, built by `python -m seminar.load` (`README.md`; not committed, so not present in the repo); Flask app (`requirements.txt`, `flask==3.1.*`); `networkx==3.7` pinned in `requirements.txt` and used only by `seminar/load.py` to read the bundled network.
- Measured, SQLite 3.53.1 in memory, with the repo's `db/schema.sql` and the 16 families and 20 ties: a recursive walk with `UNION` on (name, depth) and a depth cap of 3, grouped by minimum depth, returned the same counts as networkx `single_source_shortest_path_length` for all 16 starting families. The counts for distance up to 1, 2 and 3 were: Acciaiuoli 1, 6, 11; Albizzi 3, 10, 14; Barbadori 2, 9, 13; Bischeri 3, 8, 11; Castellani 3, 6, 11; Ginori 1, 3, 10; Guadagni 4, 9, 13; Lamberteschi 1, 4, 9; Medici 6, 11, 14; Pazzi 1, 2, 7; Peruzzi 3, 6, 10; Ridolfi 3, 11, 14; Salviati 2, 7, 11; Strozzi 4, 8, 12; Tornabuoni 3, 10, 14; Pucci 0, 0, 0 (measured).
- Timing: not measured; the arithmetic bound above is the only size figure.
- What was tried and what happened: unknown. No earlier remedy or decision record exists in the repo.
- unknown: the seminar's exact definition of "reach" (cumulative counts of families within k marriages, excluding the family itself, as used here; an exact-distance count would differ) is not stated in the request and should be confirmed with the instructor. Also unknown: whether the students' hosting environment has a Python with networkx for `seminar/load.py`, which is needed only to build the database.

## Options considered

- graph-database (Neo4j, as the colleague proposed): rejected, because the profile is absent: 16 families and 20 ties with a fixed depth of 3 is well under any budget, nothing is measured failing, and a second server would be a second copy of the data and a second thing for 25 students to run for a single panel. Learning Neo4j is a separate course goal, not a need of this workload.
- in-process-library (the graph library already pinned, networkx 3.7): rejected for the panel, because it would also meet the need (the walk is short), but the rung above it holds on the same evidence and uses the database the app already reads; networkx stays in `seminar/load.py` for the bundled data.
- recursive-sql (recursive queries on the SQLite file the app already reads): chosen, because the walk is short and fixed, the database is already operated, the required work is at most 320 row checks per depth step (arithmetic), and the recursive query matched networkx for all 16 families (measured).
- no-graph (plain joins, no traversal): rejected, because a family's reach through a second or third marriage follows ties through other families; a single join gives only the first step (one marriage).

## What would change the decision

- A requirement for reach at depths beyond 3 that grows the walk beyond what the recursive query can return for 16 families (not expected at this size) would still not change the option; a change would need a larger network, which the stated 16 families rules out.
- A larger network for later terms (for example, more families or ties than the bundled data) with a measured recursive-query time over the budget the instructor sets would move this to in-process-library, which already loads the same data.
- The instructor deciding that the seminar must teach a dedicated graph database as a goal would be a teaching decision outside the workload; the workload answer stays recursive-sql.

Nothing in the repo was changed.
