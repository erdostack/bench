FILE ?= services/routing/queries/next_hop.cypher

.PHONY: up down mgq psql test

up:
	docker compose up -d

down:
	docker compose down

# run a Cypher file against the shared Memgraph (routing)
mgq:
	services/routing/scripts/mgq.sh $(FILE)

psql:
	docker compose exec postgres psql -U postgres accounts

test:
	$(MAKE) -C services/accounts test
	cd services/gateway && npm test
	cd services/notifier && go test ./...
