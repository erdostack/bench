Decision: in-process-library. Written up in docs/graph/DECISION.md.

The register's references are a graph walked by hand: one query per level, capped at 3 because deeper searches
timed out, while chains are now 9 deep. 4,800 bylaws and 21,000 references load into networkx in 0.3 s and any
answer is under a millisecond, refreshed nightly. The clerk's rule has to go in too: only amends and depends_on
carry a repeal; a citation does not, and nothing passes through one. A graph database is a server for a dozen
clerks.
