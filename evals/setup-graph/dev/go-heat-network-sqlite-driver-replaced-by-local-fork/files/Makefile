F ?= queries/downstream_buildings.sql
ARGS ?=

.PHONY: q load test

q:
	go run ./cmd/heatq -db data/heat.db -f $(F) $(ARGS)

load:
	rm -f data/heat.db
	go run ./cmd/load -db data/heat.db -schema sql/schema.sql -csv data/csv

test:
	go test ./...
