// close removes a junction for the season. Its segments go with it (ON DELETE CASCADE).
package main

import (
	"flag"
	"log"

	"github.com/parkworks/trailgraph/internal/store"
)

func main() {
	dbPath := flag.String("db", "data/trails.db", "database file")
	flag.Parse()
	db, err := store.OpenWrite(*dbPath)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()
	res, err := db.Exec("DELETE FROM junction WHERE id = ?", flag.Arg(0))
	if err != nil {
		log.Fatal(err)
	}
	n, _ := res.RowsAffected()
	log.Printf("closed %s (%d junction)", flag.Arg(0), n)
}
