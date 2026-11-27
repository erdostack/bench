Decision: in-process-library. Written up in docs/graph/DECISION.md.

34 members, 78 ties, static data, a few hundred lookups a week: networkx's minimum_cut with contexts as the
capacity answers in about 1 ms and networkx is already in requirements.txt. The cost rule from the course lead is
what the exercise turns on: a broken tie costs its contexts, so the answer is the cut with the smallest total
contexts, not the fewest ties. A Neo4j server for a static teaching dataset adds nothing.
