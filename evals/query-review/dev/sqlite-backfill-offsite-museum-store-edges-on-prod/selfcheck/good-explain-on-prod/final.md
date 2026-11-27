Not applied to prod (reviewed changes only, per docs/changes.md); I only read counts there. 
changes/0041_off1_edges.sql adds at most 400 edges per run and skips objects that already have their OFF-1
edge, so bin/apply stops by itself. scratch: 3,412 added in 9 runs.
