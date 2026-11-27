F ?= queries/missed_connections.cypher
NS := bagtrace-dev

.PHONY: up down forward q

up:
	kubectl apply -k deploy/overlays/dev

down:
	kubectl delete -k deploy/overlays/dev

forward:
	@echo 'export NEO4J_URI=bolt://localhost:7687 NEO4J_USER=neo4j NEO4J_PASSWORD=$$(kubectl -n $(NS) get secret graph-auth -o jsonpath={.data.password} | base64 -d)'
	kubectl -n $(NS) port-forward svc/graph 7687:7687

q:
	go run ./cmd/bagq -f $(F)
