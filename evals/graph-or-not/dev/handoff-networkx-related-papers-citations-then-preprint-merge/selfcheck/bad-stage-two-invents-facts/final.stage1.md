Decision: in-process-library. Written up in docs/graph/DECISION.md.

The panel misses its 250 ms budget because the three hops are fanned out from application code (1.4 s p95), and a
recursive CTE only got to 900 ms. The 600,000 papers and 4.2M citations fit in networkx in 1.8 GB of a 6 GB pod and
the panel takes 40 ms, rebuilt after the nightly load. Your lead's rule settles the rest: no new datastore while the
in-process graph stays under 4 GB; past 4 GB, move to the platform team's graph database.
