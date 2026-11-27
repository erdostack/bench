FILE ?= queries/graft_lineage.cypher

.PHONY: up down query import test

up:
	docker compose up -d

down:
	docker compose down

# run one saved query, read-only
query:
	./scripts/run_query.sh $(FILE)

# load the planting register (orchard manager only)
import:
	python -m orchard.tools.import_register register/

test:
	python -m pytest -q
