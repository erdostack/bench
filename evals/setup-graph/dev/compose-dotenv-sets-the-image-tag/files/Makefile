.PHONY: up down seed q test

up:
	docker compose up -d --wait

down:
	docker compose down

seed:
	go run ./cmd/seed db/seed.cypher

q:
	go run ./cmd/cq $(F)

test:
	go test ./...
