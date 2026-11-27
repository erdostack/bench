.PHONY: migrate test

migrate:
	docker compose -f ../../compose.yaml exec -T postgres psql -U postgres accounts < migrations/001_init.sql

test:
	uv run pytest -q
