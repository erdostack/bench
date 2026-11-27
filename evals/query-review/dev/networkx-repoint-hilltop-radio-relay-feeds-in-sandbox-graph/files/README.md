# txplan

Wexcombe Community Radio's transmission network as a directed graph: the studio, the relays and the
low-power transmitters, stored as NetworkX node-link JSON (`docs/graph.md`).

- `bin/gx <target> <change.py>`: load a target graph, call the file's `change(G)`, save the graph.
- `bin/gx <target> --show <node>`: print a node and its links.
- `bin/reset-sandbox`: copy the live graph over the sandbox.
