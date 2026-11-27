// merge deletes duplicate stations listed in a CSV (one id per line, header "id").
package main

import (
	"encoding/csv"
	"flag"
	"log"
	"os"

	"example.org/cavesurvey/internal/store"
)

func main() {
	dbPath := flag.String("db", "data/caves.db", "SQLite file")
	list := flag.String("dups", "data/duplicates.csv", "duplicate station ids")
	flag.Parse()
	f, err := os.Open(*list)
	if err != nil {
		log.Fatal(err)
	}
	rows, err := csv.NewReader(f).ReadAll()
	f.Close()
	if err != nil {
		log.Fatal(err)
	}
	db, err := store.Open(*dbPath, false)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()
	for _, r := range rows[1:] {
		if _, err := db.Exec("DELETE FROM station WHERE id = ?", r[0]); err != nil {
			log.Fatalf("station %s still in use: %v", r[0], err)
		}
	}
}
