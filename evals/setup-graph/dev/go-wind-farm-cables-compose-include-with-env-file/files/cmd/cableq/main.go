// cableq runs one Cypher file against the inter-array cable graph, in a read transaction.
package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"os"
	"strings"

	"github.com/neo4j/neo4j-go-driver/v5/neo4j"
)

func main() {
	file := flag.String("f", "", "Cypher file")
	flag.Parse()
	params := map[string]any{}
	for _, kv := range flag.Args() {
		k, v, _ := strings.Cut(kv, "=")
		params[k] = v
	}
	src, err := os.ReadFile(*file)
	if err != nil {
		log.Fatal(err)
	}
	ctx := context.Background()
	driver, err := neo4j.NewDriverWithContext(os.Getenv("NEO4J_URI"),
		neo4j.BasicAuth(os.Getenv("NEO4J_USER"), os.Getenv("NEO4J_PASSWORD"), ""))
	if err != nil {
		log.Fatal(err)
	}
	defer driver.Close(ctx)
	res, err := neo4j.ExecuteQuery(ctx, driver, string(src), params, neo4j.EagerResultTransformer,
		neo4j.ExecuteQueryWithReadersRouting())
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(strings.Join(res.Keys, "\t"))
	for _, rec := range res.Records {
		out := make([]string, len(rec.Values))
		for i, v := range rec.Values {
			out[i] = fmt.Sprint(v)
		}
		fmt.Println(strings.Join(out, "\t"))
	}
}
