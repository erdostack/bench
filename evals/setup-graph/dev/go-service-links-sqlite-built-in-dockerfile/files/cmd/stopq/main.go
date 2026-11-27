// stopq runs one SQL file against the stop network and prints the rows.
package main

import (
	"database/sql"
	"flag"
	"fmt"
	"log"
	"os"
	"strings"

	_ "github.com/mattn/go-sqlite3"
)

func main() {
	dbPath := flag.String("db", "data/stops.db", "SQLite file holding the network")
	file := flag.String("f", "", "file with one SQL query")
	flag.Parse()
	if *file == "" {
		log.Fatal("usage: stopq -db <file> -f <query.sql> [args...]")
	}
	query, err := os.ReadFile(*file)
	if err != nil {
		log.Fatal(err)
	}
	db, err := sql.Open("sqlite3", "file:"+*dbPath+"?mode=ro")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()
	args := make([]any, 0, flag.NArg())
	for _, a := range flag.Args() {
		args = append(args, a)
	}
	rows, err := db.Query(string(query), args...)
	if err != nil {
		log.Fatal(err)
	}
	defer rows.Close()
	cols, _ := rows.Columns()
	fmt.Println(strings.Join(cols, "\t"))
	values := make([]any, len(cols))
	ptrs := make([]any, len(cols))
	for i := range values {
		ptrs[i] = &values[i]
	}
	for rows.Next() {
		if err := rows.Scan(ptrs...); err != nil {
			log.Fatal(err)
		}
		out := make([]string, len(cols))
		for i, v := range values {
			out[i] = fmt.Sprint(v)
		}
		fmt.Println(strings.Join(out, "\t"))
	}
}
