# treesurvey

Volunteer tree survey tooling for Ashworth Borough Council. Surveys are graphs: trees, the streets they
stand on, and the volunteers who surveyed them, stored as NetworkX node-link JSON.

- `bin/tg show <target>`: counts of nodes and edges by kind.
- `bin/tg run <target> <script.py>`: load the target's graph, call `change(G)` from the script, save it.
- `scripts/build_training.py`: rebuilds `data/training.json` (the course graph) from scratch.
- `docs/targets.md`: the targets.

`training` is the practice graph for volunteer survey training. Trainers change it directly however they
like, before or after a session; nothing else reads it.
