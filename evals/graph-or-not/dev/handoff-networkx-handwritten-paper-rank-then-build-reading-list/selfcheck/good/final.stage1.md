Decision: in-process-library. Written up in docs/graph/DECISION.md.

The hand-written score is PageRank with a bug (the 610 papers with no references leak rank; only 13 of the top 20
agree with networkx). networkx is already installed: use nx.pagerank with the PI's damping of 0.7. A nightly batch
on 4,800 papers and 31,000 citations takes seconds; Neo4j would be a server for that.
