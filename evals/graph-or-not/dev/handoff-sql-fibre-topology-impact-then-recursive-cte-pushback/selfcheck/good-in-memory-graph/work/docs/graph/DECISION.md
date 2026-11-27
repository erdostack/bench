Decision: in-process-library

Impact walk, 2026-11-23. One service keeps the topology in networkx and serves the NOC tools.

Numbers from the conversation: 1.6M devices / 2.3M links; walks 19 hops median, 41 max; 2 s p95 budget;
hop-by-hop loop 11.2 s; WITH RECURSIVE + cycle check 7.9 s (index scans already); closure table ~9B rows;
networkx 2.9 GB, 0.4 s p95; ~3,000 link changes/day, visible within a minute.

Considered: recursive SQL (measured, too slow), graph database (works, but a new system when one service can
hold 2.9 GB), closure table (size, churn).

Change it if: more than one service needs its own copy, or the topology outgrows one box.
