FILE ?= queries/neighbours.cypher

.PHONY: graph-up graph-down load cq test vet

graph-up:
	docker compose up -d --build --wait graph

graph-down:
	docker compose down

load:
	go run ./cmd/load data

# run one saved query, read-only
cq:
	go run ./cmd/cq $(FILE)

test:
	go test ./...

vet:
	go vet ./...
