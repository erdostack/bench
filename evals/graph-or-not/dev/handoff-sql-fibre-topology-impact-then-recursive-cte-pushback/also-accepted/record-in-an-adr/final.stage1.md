Decision: in-process-library. Written up in docs/adr/0012-impact-walk.md.

The walk is the bottleneck and SQL has been measured on it: 11.2 s p95 for the loop, 7.9 s for the recursive
query, budget 2 s. networkx did it in 0.4 s on 2.9 GB. Run one impact service that holds the graph, applies
provisioning's ~3,000 changes a day as they arrive, and serves the four NOC tools over HTTP.
