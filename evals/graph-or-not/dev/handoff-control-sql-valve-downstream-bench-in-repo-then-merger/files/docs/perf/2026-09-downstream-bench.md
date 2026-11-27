# Downstream-of-valve benchmark, September 2026

Network: 410k pipes, 380k nodes, 52k valves. Walks reach up to 160 pipes from the valve.
Replayed 2,000 valve lookups from the August planner logs against a replica.

| Implementation | p95 | Memory |
|---|---|---|
| `sql/downstream.sql` (recursive CTE, index on pipe.upstream_id) | 5.2 s | n/a |
| networkx DiGraph in the planner process, `nx.descendants` | 0.21 s | 1.9 GB resident |

The CTE plan is an index scan per step; the time is in the large fan-out below trunk mains.
