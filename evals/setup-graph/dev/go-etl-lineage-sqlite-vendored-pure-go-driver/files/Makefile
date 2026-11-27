F ?= queries/upstream_path.sql
ARGS ?= mart.revenue_daily
export GOFLAGS := -mod=vendor

.PHONY: q test

q:
	go run ./cmd/lineageq -db data/lineage.db -f $(F) $(ARGS)

test:
	go test ./...
