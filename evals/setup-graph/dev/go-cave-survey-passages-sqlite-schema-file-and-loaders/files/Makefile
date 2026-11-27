F ?= queries/route_from_entrance.sql
ARGS ?= ST-214
TRIP ?=

.PHONY: q init load merge

q:
	go run ./cmd/caveq -db data/caves.db -f $(F) $(ARGS)

init:
	go run ./cmd/initdb -db data/caves.db -schema sql/schema.sql

load:
	go run ./cmd/load -db data/caves.db -stations trips/$(TRIP)/stations.csv -shots trips/$(TRIP)/shots.csv

merge:
	go run ./cmd/merge -db data/caves.db -dups data/duplicates.csv
