Position: keep

Björn, we looked at exactly this when we decided, and the decision was to do the descendants walk in Postgres with a
recursive query (recursive-sql in docs/graph/DECISION.md). It was not a matter of taste; these are the numbers:

- The folder table is 85M rows. API pods have 1 GB of memory. The tree does not fit in a pod.
- Folders move about 300 times a second at peak. A copy refreshed every 10 minutes is wrong for up to 10 minutes,
  and a share computed from a stale tree can leave someone with access to a folder that was moved out. That is a
  security bug, not a performance trade-off.
- Speed is not the problem being solved: the recursive query measured 12 ms p95 on a production replica, with a
  250 ms budget for the share call, on trees up to 60 levels deep.

If the query ever misses the 250 ms budget, or the product accepts a stale tree, it is worth reopening. Neither is
true today.
