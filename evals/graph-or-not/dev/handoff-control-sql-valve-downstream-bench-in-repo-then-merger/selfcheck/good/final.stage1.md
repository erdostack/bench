Decision: in-process-library. Written up in docs/graph/DECISION.md.

September's benchmark settles it: the recursive query is 5.2 s p95 against the 1 s objective in docs/slo.md, with
the index already used; networkx in the planner process is 0.21 s on 1.9 GB of the 8 GB pod. More indexes do not
touch the fan-out cost, and a graph database is a server we don't need when the library fits with room to spare.
