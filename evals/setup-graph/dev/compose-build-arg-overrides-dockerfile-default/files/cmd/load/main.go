// Command load replaces the graph with the CSV files in the given directory. It writes.
package main

import (
	"context"
	"encoding/csv"
	"os"
	"path/filepath"

	"github.com/neo4j/neo4j-go-driver/v5/neo4j"

	"example.org/depotwalk/internal/config"
	"example.org/depotwalk/internal/graph"
)

func main() {
	ctx := context.Background()
	driver, err := graph.Open(config.FromEnv())
	if err != nil {
		panic(err)
	}
	defer driver.Close(ctx)
	run := func(query string, params map[string]any) {
		if _, err := neo4j.ExecuteQuery(ctx, driver, query, params, neo4j.EagerResultTransformer); err != nil {
			panic(err)
		}
	}
	run("MATCH (n) DETACH DELETE n", nil)
	for _, row := range read(filepath.Join(os.Args[1], "bins.csv")) {
		run("MERGE (a:Aisle {name: $aisle}) CREATE (:Bin {code: $code, zone: $zone})-[:IN_AISLE]->(a)",
			map[string]any{"code": row[0], "aisle": row[1], "zone": row[2]})
	}
	for _, row := range read(filepath.Join(os.Args[1], "adjacent.csv")) {
		run("MATCH (a:Bin {code: $a}), (b:Bin {code: $b}) MERGE (a)-[:NEXT_TO]->(b)",
			map[string]any{"a": row[0], "b": row[1]})
	}
}

func read(path string) [][]string {
	file, err := os.Open(path)
	if err != nil {
		panic(err)
	}
	defer file.Close()
	rows, err := csv.NewReader(file).ReadAll()
	if err != nil {
		panic(err)
	}
	return rows[1:]
}
