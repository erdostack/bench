# Model

An undirected `networkx.Graph`. Nodes are bay codes (`B-0412`, `TMP-07` for temporary event bays) with
attributes `zone` (`Z-MILL`), `spaces` (int) and `kind` (`street`, `carpark` or `temporary`). Edges are
walking links between bays with `minutes` (int), only where the walk is under 12 minutes.
