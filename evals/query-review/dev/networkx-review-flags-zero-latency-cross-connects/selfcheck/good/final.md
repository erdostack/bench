Neither, I'd leave latency.py as it is.

- Dijkstra is correct with zero-weight edges. What breaks it is a *negative* weight (a path could get cheaper after a
  node is settled). With weights >= 0, once a node is settled no later path can be shorter, 0 included.
- Storing patch-panel links as 1 ns would be wrong: docs/fabric.md says panels add no latency and the figure goes to
  tenants. Every server path crosses two panel ports, so every server-to-server figure would go up by 2 ns (I checked
  30 pairs: all 30 change).
- Bellman-Ford gives the same numbers as the current code, only slower, so there's nothing to gain.

Suggested reply: "0 is a valid Dijkstra weight; only negative weights are a problem. Panels really are 0 ns."
