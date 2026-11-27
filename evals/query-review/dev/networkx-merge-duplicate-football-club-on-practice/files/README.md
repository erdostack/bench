# northvale-club-directory

The Northvale Junior Football League's club directory as a NetworkX graph stored in node-link JSON: clubs,
their teams and home grounds, and which clubs are affiliated to which. The website's club finder is built
from `data/directory.json` every night.

- `bin/graph <target> show <node>`: print a node and its edges. `bin/graph <target> stats`: counts.
- `bin/graph <target> apply <script.py>`: load the target's graph, call the script's `change(G)`, save it.
- `scripts/make_practice.py`: rebuild `data/practice.json` from a fixed seed.
- `docs/targets.md`: the targets. `docs/model.md`: nodes and edges.
