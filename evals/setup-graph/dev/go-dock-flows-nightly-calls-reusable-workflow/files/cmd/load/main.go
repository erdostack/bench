// Command load wipes the graph and loads docks.csv and flows.csv from the given directory.
package main

import (
	"context"
	"encoding/csv"
	"log"
	"os"
	"path/filepath"
	"strconv"

	"example.org/dockflow/internal/graph"
	"github.com/neo4j/neo4j-go-driver/v5/neo4j"
)

func rows(dir, name string) [][]string {
	f, err := os.Open(filepath.Join(dir, name))
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()
	all, err := csv.NewReader(f).ReadAll()
	if err != nil {
		log.Fatal(err)
	}
	return all[1:]
}

func main() {
	dir := "data"
	if len(os.Args) > 1 {
		dir = os.Args[1]
	}
	ctx := context.Background()
	drv, err := graph.Open()
	if err != nil {
		log.Fatal(err)
	}
	defer drv.Close(ctx)
	run := func(q string, p map[string]any) {
		if _, err := neo4j.ExecuteQuery(ctx, drv, q, p, neo4j.EagerResultTransformer); err != nil {
			log.Fatal(err)
		}
	}
	run("MATCH (n) DETACH DELETE n", nil)
	var docks []map[string]any
	for _, r := range rows(dir, "docks.csv") {
		capacity, _ := strconv.Atoi(r[2])
		docks = append(docks, map[string]any{"id": r[0], "name": r[1], "capacity": capacity})
	}
	run("UNWIND $rows AS r CREATE (:Dock {id: r.id, name: r.name, capacity: r.capacity})", map[string]any{"rows": docks})
	var flows []map[string]any
	for _, r := range rows(dir, "flows.csv") {
		n, _ := strconv.Atoi(r[2])
		flows = append(flows, map[string]any{"a": r[0], "b": r[1], "n": n})
	}
	run("UNWIND $rows AS r MATCH (a:Dock {id: r.a}), (b:Dock {id: r.b}) CREATE (a)-[:RIDES_TO {per_day: r.n}]->(b)",
		map[string]any{"rows": flows})
}
