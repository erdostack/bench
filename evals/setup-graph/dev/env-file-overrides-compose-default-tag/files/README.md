# ferryboard

Connection planner for a small island ferry network: ports, sailings, and which sailings you can still catch
after a late arrival.

## Quick start

    export GRAPH_PASSWORD=<choose one>
    make up            # starts the graph database
    uv sync
    make load          # loads the winter timetable from data/
    make q F=queries/next_connections.cypher

Everything goes through the Makefile; please do not call `docker compose` directly, the Makefile passes the
stack settings.

## Layout

| Path | What |
|---|---|
| `ferryboard/` | planner library and the small web API |
| `ferryboard/tools/` | command-line helpers used by the Makefile |
| `queries/` | saved Cypher |
| `data/` | timetable CSVs |
| `config/` | stack settings |
| `docs/` | notes for operators |
