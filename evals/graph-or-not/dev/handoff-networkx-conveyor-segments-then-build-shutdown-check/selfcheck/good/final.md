Added linewatch/shutdown.py. cut_off builds a networkx DiGraph of the segments except bypasses, removes the down
station, and returns every station that is not an ancestor of a dock, per the rule in docs/graph/DECISION.md.
