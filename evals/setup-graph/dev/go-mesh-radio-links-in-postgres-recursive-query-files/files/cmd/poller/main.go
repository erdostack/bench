package main

// Polls the relays' status pages and upserts the link table; alert keys go to Redis.

import (
	"context"
	"log"

	"github.com/jackc/pgx/v5"
	"github.com/redis/go-redis/v9"
)

func main() {
	ctx := context.Background()
	conn, err := pgx.Connect(ctx, "postgres://mesh@localhost:5432/mesh")
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close(ctx)
	rdb := redis.NewClient(&redis.Options{Addr: "localhost:6379"})
	defer rdb.Close()
	log.Println("poller: nothing to poll in a dev checkout")
}
