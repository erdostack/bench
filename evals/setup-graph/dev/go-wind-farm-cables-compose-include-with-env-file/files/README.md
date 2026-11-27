# arraygraph

Inter-array cable topology of the offshore wind farm: turbines, the offshore substations and every cable
section between them, with its rating and the strings it belongs to. Engineers ask "which turbines go dark
if this section trips" and "where is the next normally-open point".

## Running it

The graph runs in Docker: Neo4j 5.26.24, the default in `deploy/graph/compose.yaml`. The API container
next to it is for the dashboard and is not needed for queries.

    make up
    make q F=queries/isolated_by_section.cypher SECTION=S-0412

Copy `.env.example` to `.env` first; the query tool and the container read the login from there. The
graph is loaded by the asset team's nightly job, not from this repo.
