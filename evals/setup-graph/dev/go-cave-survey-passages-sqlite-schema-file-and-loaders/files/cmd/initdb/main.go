// initdb creates an empty survey database from sql/schema.sql.
package main

import (
	"flag"
	"log"
	"os"

	"example.org/cavesurvey/internal/store"
)

func main() {
	dbPath := flag.String("db", "data/caves.db", "SQLite file")
	schema := flag.String("schema", "sql/schema.sql", "schema file")
	flag.Parse()
	ddl, err := os.ReadFile(*schema)
	if err != nil {
		log.Fatal(err)
	}
	db, err := store.Open(*dbPath, false)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()
	if _, err := db.Exec(string(ddl)); err != nil {
		log.Fatal(err)
	}
}
