// seed loads a Cypher script, statement by statement, into the local graph. Used by `make seed` only.
package main

import (
	"context"
	"fmt"
	"os"
	"strings"

	"github.com/neo4j/neo4j-go-driver/v5/neo4j"
	"example.org/tidewatch/internal/mesh"
)

func main() {
	body, err := os.ReadFile(os.Args[1])
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	ctx := context.Background()
	driver, err := mesh.Connect(ctx)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	defer driver.Close(ctx)
	for _, stmt := range strings.Split(string(body), ";") {
		if strings.TrimSpace(stmt) == "" {
			continue
		}
		if _, err := neo4j.ExecuteQuery(ctx, driver, stmt, nil, neo4j.EagerResultTransformer); err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(1)
		}
	}
}
