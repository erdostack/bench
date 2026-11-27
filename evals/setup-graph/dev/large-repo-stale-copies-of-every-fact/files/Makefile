COMPOSE = docker compose -f ops/compose/graph.yaml
Q ?= queries/on_loan_now.cypher

.PHONY: install up down logs cq load export similar test lint

install:
	poetry install --sync

up:
	$(COMPOSE) up -d --wait

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f graph

# run one saved query read-only: make cq Q=queries/maker_network.cypher P="maker=Aldous Finch"
cq:
	poetry run python -m curio.tools.cq $(Q) $(P)

# maintainers only: replaces the shared development graph
load:
	poetry run python -m curio.tools.load data/

export:
	scripts/export_graph.sh

similar:
	poetry run python -m curio.similarity.build --out var/similar_makers.json

test:
	poetry run pytest -q

lint:
	poetry run ruff check .
