Rewrote cutoff_segments in winter/cutoff.py as recorded in docs/graph/DECISION.md: the roads go into a
networkx MultiGraph (two roads between the same junctions stay two segments), its bridges are the segments
with no way round, and a bridge goes on the list only if closing it cuts at least one house off from the
depot. networkx needs installing on the machine that runs the report.
