// Command q runs one query file in a read transaction and prints each row as JSON.
package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"strings"

	"github.com/neo4j/neo4j-go-driver/v5/neo4j"
)

func main() {
	file := flag.String("f", "", "query file")
	flag.Parse()
	text, err := os.ReadFile(*file)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(2)
	}
	params := map[string]any{}
	for _, kv := range flag.Args() {
		if k, v, ok := strings.Cut(kv, "="); ok {
			params[k] = v
		}
	}
	user, pass, _ := strings.Cut(os.Getenv("NEO4J_AUTH"), "/")
	ctx := context.Background()
	driver, err := neo4j.NewDriverWithContext("neo4j://localhost:7687", neo4j.BasicAuth(user, pass, ""))
	if err != nil {
		panic(err)
	}
	defer driver.Close(ctx)
	res, err := neo4j.ExecuteQuery(ctx, driver, string(text), params, neo4j.EagerResultTransformer,
		neo4j.ExecuteQueryWithReadersRouting())
	if err != nil {
		panic(err)
	}
	for _, rec := range res.Records {
		line, _ := json.Marshal(rec.AsMap())
		fmt.Println(string(line))
	}
}
