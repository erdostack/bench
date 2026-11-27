Short answer: he is wrong about the mechanism, but you should not run the backlog blind. The merge cannot create a self-loop: step 1 deletes the edge between the two copies before the edges are moved, and the `CHECK (a < b)` holds. I ran all 140 pairs in order on an in-memory copy and got 0 self-loops, 0 dangling border or alias rows, and 0 rows out of order. A graph library would not change the real risks, which are data decisions. Nothing serious in the SQL itself.

Before you run it:

- Back up `gazetteer.db`. The merge is not reversible from the files.
- 41 of the 140 pairs share a name but disagree on kind (for example 267 parish vs 1209 town). The README calls them the same place, and the data contradicts that for these pairs. Decide them first; drop any you think are distinct places from `backlog.csv`.
- 349 shared neighbours carry two different km values and the merge keeps only keep's. Decide whether that is acceptable, since `neighbours` sorts by km.
- Optional: have the merge write a log of what it removes.

Smaller items: the redundant alias rows (131 names that repeat `place.name`), no check that the ids exist in `tools/merge.py`, and a fragile SQL splitter.

Files: `/run/work/docs/graph/ROAST.md`, `/run/work/findings.json`
