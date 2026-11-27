merge_duplicates is in model/clean.py. It works out each duplicate's survivor first, following chains
(A,B then B,C means C goes to A, as docs/model.md says; a pair-by-pair fold would send C to B after B was
already removed), then rebuilds the graph with every pipe mapped onto the survivors. Pipes whose two ends
land on the same manhole are dropped (the digitiser links between records, both directions), since the
solver rejects self-loops; where the kept manhole already has a pipe, its own attributes stay. On today's
data: 124 duplicates removed, 1,400 manholes left, no self-loops and no pipe pointing at a removed manhole.
Check with `nx.number_of_selfloops(H)` and `[e for e in H.edges if e[0] not in H or e[1] not in H]`.
