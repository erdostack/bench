.PHONY: up q

up:
	docker compose up -d

q:
	FIBRE_PASSWORD=$$(cut -d/ -f2 < .env) go run ./cmd/fq $(F)
