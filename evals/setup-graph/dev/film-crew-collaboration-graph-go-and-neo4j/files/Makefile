F ?= queries/worked_together.cypher
P ?= pers-0042

q:
	go run ./cmd/crewq -f $(F) -p person=$(P)

load:
	go run ./cmd/load -in data/credits.csv
