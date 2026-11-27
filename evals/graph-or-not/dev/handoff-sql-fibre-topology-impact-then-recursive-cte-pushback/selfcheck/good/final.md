Position: keep

Thanks Marta. We looked at exactly this before deciding (docs/graph/DECISION.md): we're moving the impact walk to a
graph database fed from provisioning's changes. The recursive query was measured, with a cycle check, on a
snapshot: 7.9 s p95 against the NOC's 2 s budget, and its plan was already index scans all the way down. The time
goes on the paths around the rings (median 19 hops, up to 41 over 1.6M devices and 2.3M links), which a covering
index doesn't change, and the CYCLE clause is that same cycle check. A closure table came to about 9 billion rows
and would have to follow 3,000 changes a day. Today's loop is 11.2 s.
