COMPOSE := docker compose -f compose.yaml

.PHONY: up down q

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

q:
	dotnet run --project tools/FerryQuery -- $(F)
