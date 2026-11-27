# Pruning

Every night `python -m jobs.prune` loads `data/network.json`, applies `prune(G, cutoff)` with a cutoff ten
years back, and writes it back. A record older than the cutoff is no longer evidence the interaction still
happens:

1. interactions (edges) not seen since the cutoff are removed;
2. species (nodes) not seen since the cutoff are removed, with their interactions;
3. species left with no interactions at all are removed too: the atlas has no page for a species without
   partners.

`prune` returns `(edges_removed, nodes_removed)` for the job log.
