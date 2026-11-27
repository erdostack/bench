// Package graph opens the Neo4j driver from NEO4J_URI.
package graph

import (
	"os"

	"github.com/neo4j/neo4j-go-driver/v5/neo4j"
)

func Open() (neo4j.DriverWithContext, error) {
	uri := os.Getenv("NEO4J_URI")
	if uri == "" {
		uri = "bolt://localhost:7687"
	}
	return neo4j.NewDriverWithContext(uri, neo4j.NoAuth())
}
