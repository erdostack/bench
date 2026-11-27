Decision: in-process-library. Recorded in docs/adr/0005-pipe-plan.md.

Connecting every valve at least cost is a minimum spanning tree: 212 valves and 1,900 candidate runs take about
20 ms in networkx, a few times a year. The current nearest-next walk is what wastes pipe (the tree needs 9% less
trench). The contractor's rule belongs in the weights: a run that crosses the farm track counts as its length plus
40. A graph database is a server for a script you run a few times a year.
