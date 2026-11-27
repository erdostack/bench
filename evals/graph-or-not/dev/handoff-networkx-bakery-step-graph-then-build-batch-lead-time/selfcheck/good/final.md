Added ovenplan/leadtime.py. lead_time(conn, recipe_id) loads the recipe's steps into a networkx DiGraph, counts
an untimed step as 20 minutes (the rule in docs/graph/DECISION.md), and returns the latest finish over a
topological order, so steps that don't wait on each other overlap.
