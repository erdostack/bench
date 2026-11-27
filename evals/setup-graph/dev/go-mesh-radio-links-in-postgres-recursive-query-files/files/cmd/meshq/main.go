package main

// Runs one saved SQL file against the mesh database and prints each row tab-separated.

import (
	"context"
	"fmt"
	"os"
	"strings"

	"github.com/jackc/pgx/v5"
)

func main() {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: meshq <file.sql>")
		os.Exit(2)
	}
	sql, err := os.ReadFile(os.Args[1])
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	url := os.Getenv("MESH_DB")
	if url == "" {
		url = "postgres://mesh@localhost:5432/mesh"
	}
	ctx := context.Background()
	conn, err := pgx.Connect(ctx, url)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	defer conn.Close(ctx)
	tx, err := conn.BeginTx(ctx, pgx.TxOptions{AccessMode: pgx.ReadOnly})
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	defer tx.Rollback(ctx)
	rows, err := tx.Query(ctx, string(sql))
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	for rows.Next() {
		vals, _ := rows.Values()
		cells := make([]string, len(vals))
		for i, v := range vals {
			cells[i] = fmt.Sprint(v)
		}
		fmt.Println(strings.Join(cells, "\t"))
	}
	if err := rows.Err(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
