// importer rebuilds data/pedigree.kz from the curation team's CSV exports.
package main

import (
	"flag"
	"log"
	"os"
	"path/filepath"

	kuzu "github.com/kuzudb/go-kuzu"
)

func main() {
	dbPath := flag.String("db", "../../data/pedigree.kz", "Kuzu database directory")
	in := flag.String("in", "../../data/exports", "export directory")
	flag.Parse()
	if err := os.RemoveAll(*dbPath); err != nil {
		log.Fatal(err)
	}
	db, err := kuzu.OpenDatabase(*dbPath, kuzu.DefaultSystemConfig())
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()
	conn, err := kuzu.OpenConnection(db)
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()
	ddl, err := os.ReadFile("../../schema/pedigree.cypher")
	if err != nil {
		log.Fatal(err)
	}
	for _, stmt := range []string{string(ddl),
		"COPY Accession FROM '" + filepath.Join(*in, "accessions.csv") + "' (header=true)",
		"COPY DERIVED_FROM FROM '" + filepath.Join(*in, "derivations.csv") + "' (header=true)",
	} {
		if _, err := conn.Query(stmt); err != nil {
			log.Fatal(err)
		}
	}
}
