// load rebuilds data/heat.db from the survey CSV files.
package main

import (
	"database/sql"
	"encoding/csv"
	"flag"
	"log"
	"os"
	"path/filepath"

	_ "github.com/mattn/go-sqlite3"
)

func main() {
	dbPath := flag.String("db", "data/heat.db", "SQLite file")
	schema := flag.String("schema", "sql/schema.sql", "schema file")
	dir := flag.String("csv", "data/csv", "CSV directory")
	flag.Parse()
	db, err := sql.Open("sqlite3", "file:"+*dbPath)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()
	ddl, err := os.ReadFile(*schema)
	if err != nil {
		log.Fatal(err)
	}
	if _, err := db.Exec(string(ddl)); err != nil {
		log.Fatal(err)
	}
	load(db, filepath.Join(*dir, "nodes.csv"), "INSERT INTO node (id, kind, name) VALUES (?, ?, ?)")
	load(db, filepath.Join(*dir, "pipes.csv"), "INSERT INTO pipe (id, from_node, to_node, dn_mm, length_m) VALUES (?, ?, ?, ?, ?)")
}

func load(db *sql.DB, path, stmt string) {
	f, err := os.Open(path)
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()
	rows, err := csv.NewReader(f).ReadAll()
	if err != nil {
		log.Fatal(err)
	}
	for _, r := range rows[1:] {
		args := make([]any, len(r))
		for i, v := range r {
			args[i] = v
		}
		if _, err := db.Exec(stmt, args...); err != nil {
			log.Fatal(err)
		}
	}
}
