.PHONY: up down q test

up:
	docker compose up -d

down:
	docker compose down

q:
	go run ./cmd/q -f $(F) $(ARGS)

test:
	go test ./...
