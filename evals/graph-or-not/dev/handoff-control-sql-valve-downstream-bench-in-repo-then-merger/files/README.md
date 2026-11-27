# mains-planner

Maintenance planning for the water network: which customers lose supply when a valve is shut for works.

- Python 3.12; PostgreSQL 16 (the network GIS copy). Runs in one 8 GB pod.
- `sql/downstream.sql` is the walk behind the "everything downstream of this valve" screen.
- Objectives in `docs/slo.md`; measurements in `docs/perf/`.
