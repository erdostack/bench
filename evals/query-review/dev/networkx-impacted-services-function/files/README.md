# svcmap

The service map: which services call which, from a week of tracing (`data/calls.json`).

    python -m unittest discover -s tests

`svcmap.graph.load_graph(path)` builds the graph the map page draws; `svcmap.graph.neighbours`
lists the services linked to one (the map's side panel).
