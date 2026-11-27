// Command pq runs one saved Cypher file against Memgraph over Bolt.
package main

import (
	"context"
	"fmt"
	"os"

	"github.com/neo4j/neo4j-go-driver/v5/neo4j"
)

func main() {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: <file.cypher>")
		os.Exit(2)
	}
	query, err := os.ReadFile(os.Args[1])
	if err != nil {
		panic(err)
	}
	uri := getenv("POLLINET_URI", "bolt://localhost:7687")
	auth := neo4j.BasicAuth(getenv("POLLINET_USER", "neo4j"), os.Getenv("POLLINET_PASSWORD"), "")
	ctx := context.Background()
	driver, err := neo4j.NewDriverWithContext(uri, auth)
	if err != nil {
		panic(err)
	}
	defer driver.Close(ctx)
	res, err := neo4j.ExecuteQuery(ctx, driver, string(query), nil, neo4j.EagerResultTransformer,
		neo4j.ExecuteQueryWithReadersRouting())
	if err != nil {
		panic(err)
	}
	for _, rec := range res.Records {
		fmt.Println(rec.AsMap())
	}
}

func getenv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}
