cutoff_segments now closes each segment in turn and checks which junctions the depot can no longer reach;
if any of them has houses, the segment is on the list (the manager's rule in the decision record). Done
with networkx components on a MultiGraph, so parallel roads count as a way round.
