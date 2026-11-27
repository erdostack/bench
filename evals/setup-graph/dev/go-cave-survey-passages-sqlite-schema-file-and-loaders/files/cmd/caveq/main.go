// caveq runs one SQL file read-only and prints the rows tab-separated.
package main

import (
	"database/sql"
	"flag"
	"fmt"
	"log"
	"os"
	"strings"

	"example.org/cavesurvey/internal/store"
)

func main() {
	dbPath := flag.String("db", "data/caves.db", "SQLite file")
	file := flag.String("f", "", "SQL file")
	flag.Parse()
	src, err := os.ReadFile(*file)
	if err != nil {
		log.Fatal(err)
	}
	db, err := store.Open(*dbPath, true)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()
	args := make([]any, 0, flag.NArg())
	for _, a := range flag.Args() {
		args = append(args, a)
	}
	rows, err := db.Query(string(src), args...)
	if err != nil {
		log.Fatal(err)
	}
	defer rows.Close()
	cols, _ := rows.Columns()
	fmt.Println(strings.Join(cols, "\t"))
	vals := make([]sql.NullString, len(cols))
	ptrs := make([]any, len(cols))
	for i := range vals {
		ptrs[i] = &vals[i]
	}
	for rows.Next() {
		if err := rows.Scan(ptrs...); err != nil {
			log.Fatal(err)
		}
		out := make([]string, len(vals))
		for i, v := range vals {
			out[i] = v.String
		}
		fmt.Println(strings.Join(out, "\t"))
	}
}
