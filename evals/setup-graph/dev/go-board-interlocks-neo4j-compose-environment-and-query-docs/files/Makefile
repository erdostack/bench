F ?= queries/shared_directors.cypher
COMPANY ?= C-00881

.PHONY: up down q

up:
	docker compose up -d

down:
	docker compose down

q:
	set -a; . ./.env; set +a; go run ./cmd/boardq -f $(F) company=$(COMPANY)
