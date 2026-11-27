# ADR 0012: impact walk off Postgres

Status: accepted, 2026-11-23

Decision: in-process-library

The walk (19 hops median, 41 max, rings) is the bottleneck: loop 11.2 s p95, WITH RECURSIVE with a cycle check
7.9 s p95 (index scans), budget 2 s. Closure table ~9 billion rows, 3,000 changes/day. networkx: 2.9 GB, 0.4 s.
One impact service holds the graph and serves the four NOC tools.
