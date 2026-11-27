Position: keep

We decided on a graph database for the impact walk. Recursive SQL over rings and meshes is the wrong tool: every
hop multiplies the paths, and a covering index can't fix that. A graph store walks adjacency directly.
