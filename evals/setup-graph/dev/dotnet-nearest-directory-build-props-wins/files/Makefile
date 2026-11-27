.PHONY: up reset q

up:
	docker compose up -d

reset:
	docker compose exec -T memgraph mgconsole < data/families.cypherl

q:
	dotnet run --project src/Glotto.Query -- $(F)
