// load appends one trip's stations and shots from CSV.
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
	stations := flag.String("stations", "", "stations CSV")
	shots := flag.String("shots", "", "shots CSV")
	flag.Parse()
	db, err := store.Open(*dbPath, false)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()
	for _, job := range []struct{ file, stmt string }{
		{*stations, "INSERT INTO station (id, name, depth_m, survey_trip) VALUES (?, ?, ?, ?)"},
		{*shots, "INSERT INTO passage (from_station, to_station, length_m, bearing, inclination) VALUES (?, ?, ?, ?, ?)"},
	} {
		f, err := os.Open(job.file)
		if err != nil {
			log.Fatal(err)
		}
		rows, err := csv.NewReader(f).ReadAll()
		f.Close()
		if err != nil {
			log.Fatal(err)
		}
		for _, r := range rows[1:] {
			args := make([]any, len(r))
			for i, v := range r {
				args[i] = v
			}
			if _, err := db.Exec(job.stmt, args...); err != nil {
				log.Fatal(err)
			}
		}
	}
}
