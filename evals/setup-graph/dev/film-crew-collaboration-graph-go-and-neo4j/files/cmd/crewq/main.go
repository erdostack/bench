// crewq runs one saved Cypher file in a read transaction.
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
	param := flag.String("p", "", "name=value parameter")
	flag.Parse()
	query, err := os.ReadFile(*file)
	if err != nil {
		log.Fatal(err)
	}
	params := map[string]any{}
	if k, v, ok := strings.Cut(*param, "="); ok {
		params[k] = v
	}
	user, pass, _ := strings.Cut(strings.TrimPrefix(os.Getenv("NEO4J_AUTH"), ""), "/")
	ctx := context.Background()
	driver, err := neo4j.NewDriverWithContext("neo4j://localhost:7687", neo4j.BasicAuth(user, pass, ""))
	if err != nil {
		log.Fatal(err)
	}
	defer driver.Close(ctx)
	result, err := neo4j.ExecuteQuery(ctx, driver, string(query), params,
		neo4j.EagerResultTransformer, neo4j.ExecuteQueryWithReadersRouting())
	if err != nil {
		log.Fatal(err)
	}
	for _, record := range result.Records {
		fmt.Println(record.Values...)
	}
}
