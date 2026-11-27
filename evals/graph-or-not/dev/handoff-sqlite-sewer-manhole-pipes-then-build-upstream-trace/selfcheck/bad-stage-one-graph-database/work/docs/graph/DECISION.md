# Upstream list for the flooding desk

Decision: graph-database

## Workload facts (from the conversation, 2026-11-24)

- Export: about 14,200 nodes and 15,100 pipes, refreshed monthly; the desk handles about 15 floods a week, from
  a laptop.
- Network ops rule: the trace STOPS at pumping stations. Do not list the pumping station, and do not list
  anything that drains into it (that catchment is the pumping team's).
- sql/upstream_draft.sql never finishes on Eastgate: the overflow links between the trunk sewers are digitised
  both ways, so the pipe graph has loops, and the draft's hop count makes each lap a new row.

## Options considered

- graph-database (asset data lead): rejected. A server for a monthly file and 15 lookups a week.
- in-process-library: would work (networkx ancestors), but the data is already in SQLite and one query does it.
- recursive-sql: chosen. Walk pipe from ds_node to us_node, carry the node id only, do not expand through a
  pumping station.
- no-graph: rejected; the upstream set is a variable-depth walk.

## What would change the decision

- Questions about the whole network at once (critical pipes, catchment boundaries) rather than one node.
