DB ?= data/trails.db

.PHONY: load q close test

load:
	go run ./cmd/load -db $(DB)

q:
	go run ./cmd/q -db $(DB) $(F)

close:
	go run ./cmd/close -db $(DB) $(J)

test:
	go test ./...
