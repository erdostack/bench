# 0004 Interaction check

Accepted 2026-11-23; revised 2026-11-23 for nested classes.

Decision: in-process-library

History: first decided no-graph (flat class list, one join: 4 ms p95 against 200 ms, 3,000 checks a minute, 21k drugs,
140k rules). Classes now nest up to 5 levels, so the check needs each drug's ancestor classes. The formulary is
small and loaded monthly: build a drug -> ancestor classes map in memory at each load and keep the rule join in SQL.
No graph database.
