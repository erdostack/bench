package main

import (
	"context"
	"log"
	"os"
	"time"

	"github.com/redis/go-redis/v9"
)

func main() {
	addr := os.Getenv("NOTIFIER_REDIS")
	if addr == "" {
		addr = "localhost:6379"
	}
	client := redis.NewClient(&redis.Options{Addr: addr})
	ctx := context.Background()
	first, err := client.SetNX(ctx, "seen:startup", 1, time.Hour).Result()
	if err != nil {
		log.Fatal(err)
	}
	log.Printf("notifier up (first start this hour: %v)", first)
}
