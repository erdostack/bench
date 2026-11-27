FILE ?= sql/all_prereqs.sql

.PHONY: sql test

# run one saved query; the session is forced read-only
sql:
	docker compose exec -T -e PGOPTIONS='-c default_transaction_read_only=on' db \
		psql -U planner -d planner -v ON_ERROR_STOP=1 -f - < $(FILE)

test:
	pipenv run pytest -q
