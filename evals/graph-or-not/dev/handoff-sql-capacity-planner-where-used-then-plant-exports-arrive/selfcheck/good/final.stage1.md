Decision: need-more-information

The current query is out: 40,000 components x 90 ms is about an hour against your 10-minute window, and that's
on Linz alone. So the where-used has to be held in memory or in a graph store. Which one depends on whether all
three plants fit in the 2 GB ops gives the planner, and two of the three sizes are unknown. Can you get the Brno
and Pune BOM line counts, or better, load all three into networkx and measure the resident size? Under 2 GB it's
networkx in the planner; over, we look at Kai's graph database. Written up in docs/graph/DECISION.md.
