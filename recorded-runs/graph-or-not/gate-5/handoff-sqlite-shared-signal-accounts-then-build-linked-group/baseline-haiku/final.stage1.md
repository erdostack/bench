Decision: recursive-sql

Keep the linked-accounts lookup in the existing SQLite database and replace the depth-limited loop with one recursive query that follows only device and card signals. Do not move accounts and signals into a graph database.

Why:
- Trust and safety's rule is a filter on the edge kind: two accounts link only through a shared device or card. Shared IPs never link. The query below encodes that rule directly. The current code does not do this: linked_accounts in moderation/links.py joins on every signal kind, so it links accounts through shared IPs, which the rule forbids. The 31-of-400 comparison may have the same problem if the networkx reference also included IP edges. Recompute that comparison on device and card edges only before quoting it.
- The missed groups come from max_depth=3. A recursive query with UNION (not UNION ALL) runs until no new accounts appear, so the depth guard goes away and cycles end on their own.
- The work is one lookup at a time, about 200 a day, against an indexed table of 1.1M rows. A graph database would add a server and a second copy of the data for a query the existing indexes can serve. The signal table already has the primary key (account_id, kind, value) and the index signal_value (kind, value).
- An in-process graph would load 1.1M signal rows into memory to answer one question at a time. It is workable, but it adds more moving parts than this needs.

Query to try (SQLite, parameter :start):

WITH RECURSIVE linked(id) AS (
  SELECT :start
  UNION
  SELECT s2.account_id
  FROM linked JOIN signal s1 ON s1.account_id = linked.id AND s1.kind IN ('device', 'card')
  JOIN signal s2 ON s2.kind = s1.kind AND s2.value = s1.value AND s2.kind IN ('device', 'card')
)
SELECT id FROM linked ORDER BY id

Checks before relying on it:
- Run EXPLAIN QUERY PLAN on the nightly copy, and run ANALYZE first. In a small test the planner chose the signal_value index on kind alone for the account step, which would scan every device row at each step. On a synthetic copy of the stated size (240k accounts, 1.1M signals) with ANALYZE, the planner used the account index and the lookup took about 14 s for a group of 170k accounts. That data was random, not real, so it is a worst case for the plan, not a measurement of the register. Real groups are probably far smaller, but measure the largest real groups (a shared card or device used by many accounts can make a large group) against the 2-second target.
- If the largest real groups are still slow, the next step is precomputed components: a nightly union-find over device and card edges, storing a component id per account, which makes each lookup a single index read. That is a change of design, not of database, and it stays out of graph-database territory.
- Compare the new output with the networkx connected_components result on device and card edges only, not on all signals.

Note for the panel: panel() in moderation/panel.py still calls the old function and carries a TODO for this decision. Once the query is in place, the panel should call it, and the ban-evasion view should say which signal kinds the link is based on.
