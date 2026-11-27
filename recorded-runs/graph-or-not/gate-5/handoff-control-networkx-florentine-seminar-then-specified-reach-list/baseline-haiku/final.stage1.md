Decision: in-process-library

Build the marriage graph in memory with networkx, which is already in requirements.txt, and compute reach with a breadth-first search from each family. Do not put the network into Neo4j for the panel.

Why:
- "How many families can this family reach through one, two or three marriages" is a traversal, so it is a graph problem and "no-graph" is wrong. But the network is 16 families and 20 ties, it never changes, and it is served by a Flask app. A breadth-first search over 16 nodes returns in well under a millisecond. Any of the other options works, and the cheapest one that the project already has is the library.
- A graph database would add a server, a driver and a second copy of the data for no gain in this app. Teaching Neo4j is a fine goal for a seminar exercise, but it is not a reason to change the production panel. If students should learn Neo4j, a separate exercise that loads the same seminar.db into Neo4j would keep the app simple.
- Recursive SQL on marriage_tie would also work at this size: a recursive CTE with a depth limit of 3 and UNION to drop repeats. It is a reasonable alternative if the team wants to keep the app free of networkx. The library version is shorter and easier for students to read.

Implementation notes for the reach panel in seminar/app.py:
- Build the graph from the family table as well as marriage_tie. Pucci has no ties, so it appears only in family. If nodes come only from edges, Pucci is dropped and its page breaks.
- Decide whether "reach in two" means families at exactly two marriages or within two marriages. Within is the usual reading. Return three counts for each family, one for each depth, and exclude the family itself.
- nx.single_source_shortest_path_length(g, family, cutoff=3) gives the distance to each reachable family in one call, and counting distances <= 1, <= 2 and <= 3 gives the three numbers.
- Test with a fixture: an isolated family (Pucci) shows 0 at every depth; a family with a chain of length 3 shows a count at depth 3 and not at depth 2.

Caveat: this decision is based on the schema, the loader and the sizes given in the request. The panel has not been built or run, and the seminar.db file was not built here.
