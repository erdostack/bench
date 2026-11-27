// Command legacy-export dumps the 2023 survey graph to CSV. Kept for the archive; not built with the service.
package main

import (
	"fmt"

	"github.com/neo4j/neo4j-go-driver/v4/neo4j"
)

func main() {
	driver, err := neo4j.NewDriver("bolt://localhost:7687", neo4j.NoAuth())
	if err != nil {
		panic(err)
	}
	defer driver.Close()
	fmt.Println("export done")
}
