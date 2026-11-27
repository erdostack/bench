Decision: recursive-sql

Finding the payer is a walk up the parent chain: the highest org at or above the starting org that has its own billing account, otherwise the org itself. That is a real traversal (so not no-graph), but a tiny one. Hierarchies are at most 6 levels and there are 14,000 orgs, so the monthly run touches at most 14,000 x 6 = 84,000 chain rows. A recursive query on the SQLite database you already run does it by primary-key lookups, so I would not adopt Neo4j or another graph database, and an in-memory graph library would add a loader for no gain.

Numbers it turns on:
- On a synthetic 14,000-org tree (up to 6 levels, 400 dangling parents; not your real data), one recursive query for all orgs took about 0.13 s, and a single tooltip lookup about 0.015 ms. The plan used the primary key at every step.
- The 412 orphans (about 2.9% of orgs) are handled by the query itself. Joining the child to org.id = parent_id returns no row for a deleted parent, so the chain ends at the last org that exists, as Finance asked, with no default org and no guessing.

Things to build in (I changed no code; the only file I added is docs/graph/DECISION.md):
- Cap the recursion depth (say 20), because with foreign keys off nothing stops a cycle, and the 6-level limit is stated but not enforced.
- Pick the ancestor with an account at the greatest depth up (highest in the hierarchy), and fall back to the org itself when no one in the chain has an account.

What I could not find or measure: the real var/billing.db (not in the repo), so the real depth distribution, any cycles and real timings are unknown, and so is the tooltip's latency budget. If the real data goes deeper than 6, grows by orders of magnitude, or misses a budget after a plan check, revisit an in-process library; a graph database stays unwarranted at this size.
