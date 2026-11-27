// Command q runs one saved Cypher query read-only and prints the rows tab-separated.
package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"strings"

	"example.org/dockflow/internal/graph"
	"github.com/neo4j/neo4j-go-driver/v5/neo4j"
)

func main() {
	if len(os.Args) != 2 {
		log.Fatal("usage: q <file.cypher>")
	}
	text, err := os.ReadFile(os.Args[1])
	if err != nil {
		log.Fatal(err)
	}
	ctx := context.Background()
	drv, err := graph.Open()
	if err != nil {
		log.Fatal(err)
	}
	defer drv.Close(ctx)
	res, err := neo4j.ExecuteQuery(ctx, drv, string(text), nil, neo4j.EagerResultTransformer,
		neo4j.ExecuteQueryWithReadersRouting())
	if err != nil {
		log.Fatal(err)
	}
	for _, rec := range res.Records {
		cells := make([]string, len(rec.Values))
		for i, v := range rec.Values {
			cells[i] = fmt.Sprint(v)
		}
		fmt.Println(strings.Join(cells, "\t"))
	}
}
