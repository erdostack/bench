Decision: in-process-library. Written up in docs/graph/DECISION.md.

The walk is the bottleneck and MySQL has been measured on it: 6.1 s for the loop, 2.4 s for the recursive query on
the index, budget 500 ms. In the registry service the same walk is 38 ms on 6 GB of a 32 GB host, with publish
events applied live. Your lead's rule keeps it in-process while it fits in half a host (16 GB); a graph database
is the next step when it doesn't.
