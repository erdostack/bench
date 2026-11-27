Rewrote group_records in dedupe/link.py as recorded in docs/graph/DECISION.md: records are nodes, a shared email or
phone is an edge (address is ignored, per product), and the groups are networkx's connected components, so a
record that links two existing groups merges them. Every record appears once; records with no match are groups of
one. You'll need networkx in requirements.txt; I left that file alone.
