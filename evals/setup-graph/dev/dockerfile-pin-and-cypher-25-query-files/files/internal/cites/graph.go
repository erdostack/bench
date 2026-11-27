// Package cites holds the one place this repo opens a connection to the graph.
package cites

import (
	"context"
	"os"

	"github.com/neo4j/neo4j-go-driver/v5/neo4j"
)

func getenv(name, fallback string) string {
	if v := os.Getenv(name); v != "" {
		return v
	}
	return fallback
}

// Connect opens a driver for the local graph. The caller closes it.
func Connect(ctx context.Context) (neo4j.DriverWithContext, error) {
	uri := getenv("CITEGRAPH_BOLT", "bolt://localhost:7687")
	auth := neo4j.BasicAuth("neo4j", os.Getenv("CITEGRAPH_PASSWORD"), "")
	return neo4j.NewDriverWithContext(uri, auth)
}

// ReadRows runs a query routed to readers and returns every record as a map.
func ReadRows(ctx context.Context, query string, params map[string]any) ([]map[string]any, error) {
	driver, err := Connect(ctx)
	if err != nil {
		return nil, err
	}
	defer driver.Close(ctx)
	result, err := neo4j.ExecuteQuery(ctx, driver, query, params,
		neo4j.EagerResultTransformer, neo4j.ExecuteQueryWithReadersRouting())
	if err != nil {
		return nil, err
	}
	rows := make([]map[string]any, 0, len(result.Records))
	for _, record := range result.Records {
		rows = append(rows, record.AsMap())
	}
	return rows, nil
}
