.PHONY: up down q poll

up:
	docker compose --env-file deploy/local.env up -d

down:
	docker compose --env-file deploy/local.env down

poll:
	go run ./cmd/poller

q:
	go run ./cmd/meshq $(F)
