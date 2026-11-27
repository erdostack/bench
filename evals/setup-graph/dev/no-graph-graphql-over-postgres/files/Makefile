.PHONY: run migrate psql test

run:
	uvicorn app.main:app --reload

migrate:
	for f in migrations/*.sql; do docker compose exec -T db psql -U tally -d tally -f - < $$f; done

psql:
	docker compose exec db psql -U tally -d tally

test:
	pytest -q
