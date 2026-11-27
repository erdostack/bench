# 0007. Critical stops for the nightly planning report

Status: Accepted
Date: 2026-11-23

Decision: in-process-library

## Workload (as stated by the planning team, 2026-11-23)

- Ops' definition: a stop is critical if closing it leaves part of the network unable to reach the rest. Not
  ranked by boardings. In graph terms: the cut vertices (articulation points) of the network, links read as
  undirected (trams run both ways).
- Network: about 3,100 stops and 3,900 links; changes a few times a year.
- Runs once a night in the report job; 40 minute window; nobody waits on it.
- Team: 3 analysts, Python and pandas; nobody to operate a server.

## Options

- graph-database: rejected. A server to run and feed nightly, for a graph of a few thousand nodes.
- in-process-library: chosen. Load `stop`/`link` from the planning db into networkx, `articulation_points`.
- recursive-sql: rejected. Cut vertices are not a walk from one start stop.
- no-graph: rejected. Connectivity of the whole network is the question.

## What would change this

- Ops wanting this live, during the day, against the timetable system rather than the nightly copy.
