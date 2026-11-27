Decision: in-process-library

Keep networkx in the app and fix how it is used. The control room's rule is least driving minutes for a truck
that cannot use bus gates; the code counts segments and loads into an nx.Graph, which keeps only the last of two
rows between the same junctions (so a bus gate can hide the old road beside it). Load the segments without bus
gates into a MultiGraph (or keep the fastest legal row per pair) and run Dijkstra on minutes. 8,100 segments, 4
depots, 30 breakdowns a day: milliseconds. The vendor's graph database would move routing into a system we don't
run for a fix that is three lines. Recorded in docs/graph/DECISION.md.
