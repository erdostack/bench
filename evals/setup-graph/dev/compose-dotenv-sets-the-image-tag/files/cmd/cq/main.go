// cq runs one saved Cypher file against the buoy mesh graph in a read session and prints each row as JSON.
package main

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"time"

	"example.org/tidewatch/internal/mesh"
)

func main() {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: cq <file.cypher>")
		os.Exit(2)
	}
	body, err := os.ReadFile(os.Args[1])
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	ctx, cancel := context.WithTimeout(context.Background(), 60*time.Second)
	defer cancel()
	rows, err := mesh.ReadRows(ctx, string(body), nil)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	enc := json.NewEncoder(os.Stdout)
	for _, row := range rows {
		_ = enc.Encode(row)
	}
}
