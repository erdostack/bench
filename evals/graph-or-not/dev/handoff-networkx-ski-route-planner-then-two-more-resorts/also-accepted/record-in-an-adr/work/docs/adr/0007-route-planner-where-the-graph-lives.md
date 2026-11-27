# 0007. Route planner: where the graph lives

Status: Accepted
Date: 2026-11-23

Decision: in-process-library

## Workload (stated 2026-11-23)

- Network: 1,800 nodes, 4,200 edges; edited by ops about twice a season.
- Planner memory: 140 MB of a 2 GB pod.
- Route latency: 22 ms p95; budget 300 ms. Peak about 60 route requests/s (powder days).

## Options

- graph-database (vendor pitch): rejected; adds a hop and a system to a sub-budget in-memory answer.
- in-process-library: chosen (what runs today).
- recursive-sql: rejected; weighted shortest paths with grade filters, no SQL store in this service.
- no-graph: rejected; routing is the product.

## What would change this

- Planner memory approaching the pod size, or p95 approaching the 300 ms budget under peak load.
- The network changing continuously (live lift closures fed in per minute).
