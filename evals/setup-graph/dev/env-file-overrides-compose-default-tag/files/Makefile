COMPOSE := docker compose --env-file config/stack.env
F ?= queries/next_connections.cypher

.PHONY: up down logs load q test lint

up:
	$(COMPOSE) up -d --wait graph

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f graph

load:
	uv run python -m ferryboard.tools.load data/

# run one saved query (read-only)
q:
	./scripts/q.sh $(F)

test:
	uv run pytest -q

lint:
	uv run ruff check .
