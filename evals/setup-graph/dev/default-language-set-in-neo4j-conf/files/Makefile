include config/local
export

FILE ?= queries/huts_within_a_day.cypher

.PHONY: up down load query test

up:
	docker compose up -d --wait graph

down:
	docker compose down

load:
	uv run python -m trailmap.tools.load data/

query:
	uv run python -m trailmap.tools.run $(FILE)

test:
	uv run pytest -q
