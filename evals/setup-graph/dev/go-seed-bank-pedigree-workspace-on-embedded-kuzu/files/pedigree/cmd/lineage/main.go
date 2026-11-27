// lineage runs one Cypher file against the pedigree database, read-only.
package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"strings"

	kuzu "github.com/kuzudb/go-kuzu"
)

func main() {
	dbPath := flag.String("db", "data/pedigree.kz", "Kuzu database directory")
	file := flag.String("f", "", "Cypher file")
	flag.Parse()
	params := map[string]any{}
	for _, kv := range flag.Args() {
		k, v, _ := strings.Cut(kv, "=")
		params[k] = v
	}
	src, err := os.ReadFile(*file)
	if err != nil {
		log.Fatal(err)
	}
	cfg := kuzu.DefaultSystemConfig()
	cfg.ReadOnly = true
	db, err := kuzu.OpenDatabase(*dbPath, cfg)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()
	conn, err := kuzu.OpenConnection(db)
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()
	stmt, err := conn.Prepare(string(src))
	if err != nil {
		log.Fatal(err)
	}
	res, err := conn.Execute(stmt, params)
	if err != nil {
		log.Fatal(err)
	}
	defer res.Close()
	for res.HasNext() {
		row, _ := res.Next()
		values, _ := row.GetAsSlice()
		fmt.Println(values...)
	}
}
