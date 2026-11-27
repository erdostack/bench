F ?= queries/isolated_by_section.cypher
SECTION ?= S-0412

.PHONY: up down q

up:
	docker compose up -d graph

down:
	docker compose down

q:
	set -a; . ./.env; set +a; go run ./cmd/cableq -f $(F) section=$(SECTION)
