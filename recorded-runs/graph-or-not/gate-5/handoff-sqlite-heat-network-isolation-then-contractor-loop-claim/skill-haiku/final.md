Position: keep

The contractor is wrong about this query. The walk in sql/isolate.sql terminates on the ring mains, and we have not changed the decision, which is recursive-sql on the SQLite network file.

Why it terminates: the recursive step uses UNION over the node id alone. A node reached again by another route is dropped, so the walk stops when it reaches nodes it has already seen. The comment in the SQL says so, and the query has only the node id to keep. The loop risk would come back if someone changed it to UNION ALL or added a path column, so that should stay a review point.

The numbers:
- Present timing: p95 35 ms on the full network, against a 2 s budget (stated by you). That is about 60 times headroom. At about 40 isolations a day the total is about 1.4 s a day.
- Synthetic check of the same size (1,900 nodes, 2,400 pipes): a random topology gave p95 32.5 ms with all 1,900 nodes reached, and a ring topology gave p95 28.6 ms, max 61.7 ms, with all 2,400 isolations completing.
- Loop check, run this session: a 5-node ring returned the right answer and stopped. A 1,900-node ring with 501 chords, 300 isolations: p50 9.6 ms, p95 17.3 ms, max 25.1 ms, every run finished. This test used a different generator from the one in the record, so treat it as a termination check, not a new timing.

What would change this: the measured p95 on the real var/heatnet.db going above 2 s, a request for a batch run over all pipes, or isolation volume rising to many calls per second. Each would be checked by measuring on the real file first. A graph database would only come up if SQL is measured failing at the needed depth after the plan and index checks. Neo4j would also add a second stateful server to run, and a feed from the asset register that can drift.

Nothing in the repo was changed, and the decision record is as it was.
