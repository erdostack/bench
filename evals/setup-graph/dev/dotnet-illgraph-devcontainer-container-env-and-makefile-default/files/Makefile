GRAPH_TAG ?= 5.26.24-community
F ?= queries/slow_routes.cypher

.PHONY: graph-up graph-down seed q

graph-up:
	docker run -d --name illgraph-neo4j --env-file graph.env -p 7474:7474 -p 7687:7687 \
	  -v illgraph-data:/data neo4j:$(GRAPH_TAG)

graph-down:
	docker rm -f illgraph-neo4j

seed:
	set -a; . ./graph.env; set +a; dotnet run --project src/IllGraph.Query -- --write schema/constraints.cypher

q:
	set -a; . ./graph.env; set +a; dotnet run --project src/IllGraph.Query -- $(F)
