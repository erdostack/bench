Decision: in-process-library

It is a longest path through each recipe's step graph: about 26 steps, 1,800 recipes, all in one SQLite file. Even
150 opens x 400 products is trivial for networkx, which you already ship. A graph database would be a server to
keep in sync with the bakers' file for graphs of 26 nodes. The 20-minute rule for untimed steps goes into the node
durations. I put the decision and the rule in docs/graph/DECISION.md.
