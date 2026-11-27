// Package graph wraps the driver: one place that knows how to connect and how to run a read query.
package graph

import (
	"context"

	"github.com/neo4j/neo4j-go-driver/v5/neo4j"

	"example.org/depotwalk/internal/config"
)

func Open(cfg config.Config) (neo4j.DriverWithContext, error) {
	return neo4j.NewDriverWithContext(cfg.GraphURI, neo4j.BasicAuth(cfg.GraphUser, cfg.GraphPassword, ""))
}

// Read runs a query against a reader and returns every row as a map.
func Read(ctx context.Context, driver neo4j.DriverWithContext, query string, params map[string]any) ([]map[string]any, error) {
	result, err := neo4j.ExecuteQuery(ctx, driver, query, params, neo4j.EagerResultTransformer,
		neo4j.ExecuteQueryWithReadersRouting())
	if err != nil {
		return nil, err
	}
	rows := make([]map[string]any, 0, len(result.Records))
	for _, record := range result.Records {
		rows = append(rows, record.AsMap())
	}
	return rows, nil
}
