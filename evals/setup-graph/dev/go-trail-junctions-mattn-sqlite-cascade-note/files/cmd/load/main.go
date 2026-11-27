// load rebuilds the database from db/schema.sql and data/junctions.csv, data/segments.csv.
package main

import (
	"encoding/csv"
	"flag"
	"log"
	"os"

	"github.com/parkworks/trailgraph/internal/store"
)

func rows(path string) [][]string {
	f, err := os.Open(path)
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
	dbPath := flag.String("db", "data/trails.db", "database file")
	flag.Parse()
	os.Remove(*dbPath)
	db, err := store.OpenWrite(*dbPath)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()
	schema, _ := os.ReadFile("db/schema.sql")
	if _, err := db.Exec(string(schema)); err != nil {
		log.Fatal(err)
	}
	for _, r := range rows("data/junctions.csv") {
		db.Exec("INSERT INTO junction VALUES (?, ?, ?, ?)", r[0], r[1], r[2], r[3])
	}
	for _, r := range rows("data/segments.csv") {
		db.Exec("INSERT INTO segment VALUES (?, ?, ?, ?, ?)", r[0], r[1], r[2], r[3], r[4])
	}
}
