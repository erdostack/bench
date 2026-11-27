Rewrote pipe_layout in irrigation/layout.py as recorded in docs/graph/DECISION.md: networkx minimum spanning
tree over the candidate runs, where a run that crosses the farm track costs its length plus 40 (the
contractor's boring rule). Every valve is fed and there are no loops. networkx isn't in a requirements file
yet; you'll need to install it on the machine that runs plan.py.
