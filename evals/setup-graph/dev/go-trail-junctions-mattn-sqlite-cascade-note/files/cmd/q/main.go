// q runs one SQL file against the trail database and prints the rows, tab-separated.
package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"strings"

	"github.com/parkworks/trailgraph/internal/store"
)

func main() {
	dbPath := flag.String("db", "data/trails.db", "database file")
	flag.Parse()
	text, err := os.ReadFile(flag.Arg(0))
	if err != nil {
		log.Fatal(err)
	}
	db, err := store.OpenRead(*dbPath)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()
	rows, err := db.Query(string(text))
	if err != nil {
		log.Fatal(err)
	}
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
