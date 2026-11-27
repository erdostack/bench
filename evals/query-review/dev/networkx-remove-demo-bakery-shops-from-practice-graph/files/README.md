# droproutes

Millrace Bakery's delivery network as a directed graph in GraphML: depots and the shops they deliver to,
and the stock transfers between depots (`docs/network.md`). The route planner reads it.

- `bin/net <target> <change.py>`: load a target graph with NetworkX, call the file's `change(G)`, save it.
- `bin/new-practice`: rebuild the practice graph (a copy of the network plus the training shops).
