// Command cq runs one saved query file read-only and prints each row.
package main

import (
	"context"
	"fmt"
	"os"

	"example.org/depotwalk/internal/config"
	"example.org/depotwalk/internal/graph"
)

func main() {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: go run ./cmd/cq <file.cypher>")
		os.Exit(2)
	}
	query, err := os.ReadFile(os.Args[1])
	if err != nil {
		panic(err)
	}
	ctx := context.Background()
	driver, err := graph.Open(config.FromEnv())
	if err != nil {
		panic(err)
	}
	defer driver.Close(ctx)
	rows, err := graph.Read(ctx, driver, string(query), nil)
	if err != nil {
		panic(err)
	}
	for _, row := range rows {
		fmt.Println(row)
	}
}
