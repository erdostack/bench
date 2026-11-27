// heatq runs one SQL file against the heat network and prints the rows tab-separated.
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
	dbPath := flag.String("db", "data/heat.db", "SQLite file")
	file := flag.String("f", "", "SQL file to run")
	flag.Parse()
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
	vals := make([]any, len(cols))
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
			out[i] = fmt.Sprint(v)
		}
		fmt.Println(strings.Join(out, "\t"))
	}
}
