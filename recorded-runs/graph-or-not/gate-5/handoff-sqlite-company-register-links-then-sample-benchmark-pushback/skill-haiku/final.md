Position: keep

Marta, the 0.4 s is a fair measurement of the wrong thing. var/sample.db is a synthetic 20,000-entity, 60,000-relation file from tools/make_sample.py, and the register is 48M entities and 310M relations in one 41 GB file. We have not dropped the graph database plan, and we have not chosen SQLite either: the decision on record is still need-more-information.

What I re-ran on a fresh synthetic sample (read-only, nothing in the repo changed):
- linked_within at 6 hops, unreachable target so the full walk runs, 20 random starts: p50 0.158 s, max 0.307 s. Your 0.4 s is the same order.
- From one start, 50,866 route rows at 6 hops reach 17,208 distinct entities. The query returns one row per route, so it does far more work than the entities it reaches.
- Average degree on the register is 12.9 (2 x 310M / 48M), so an average start gives 12.9^6 = 4.6M routes, about 90 times the sample at the same depth. A linear extrapolation gives about 14 s at p50, before hub starts and before cache misses on a 41 GB file. That is an estimate, not a measurement.

What would move the decision:
1. The share of real 6-link calls that touch a hub within three links, and the distinct entities each reaches. Counted from the analysts' query log on a read-only copy.
2. p50, p95 and timeout count for linked_within on real calls, with the total call count as the denominator.
3. For Neo4j: its version, Cypher version, a full 310M-relation copy, and p95 at 25 concurrent analyst questions.
4. EXPLAIN QUERY PLAN of linked_within on the full file, read-only.

A tuned SQLite version (one statement, deduplicated nodes, both directions) is worth writing and running on the full file. It is not a reason to drop the graph database plan until it passes the 10 s test there.

Full reasoning is in docs/graph/DECISION.md.
