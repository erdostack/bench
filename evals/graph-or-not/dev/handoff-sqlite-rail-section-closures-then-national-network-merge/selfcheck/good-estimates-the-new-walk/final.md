Decision: in-process-library

The desk needs an answer within 1 s. On the merged network the recursive query is 7.4 s p95 with the index
lookups already in the plan, so it is more than seven times over; more cores do not make one SQLite query faster.
Load the nightly export into networkx instead: 380,000 sections take a few hundred MB, well inside the 8 GB box,
and a connected-component walk from the closed section answers in about 300 ms. docs/graph/DECISION.md now says
in-process-library.
