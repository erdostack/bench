# pollinet

Plant-pollinator interaction network from volunteer surveys. Nodes are species (`kind` = "plant" or
"pollinator", `last_seen` = date of the latest survey record); an edge means the pollinator was recorded
visiting the plant (`seen` = latest date, `visits` = count).

- `data/network.json`: the network (networkx node-link JSON). The atlas pages read it.
- `jobs/prune.py`: the nightly prune, see `docs/pruning.md`. Tests: `python3 -m unittest`.
