// Package routes answers the planner's questions.
package routes

import (
	"context"

	"github.com/neo4j/neo4j-go-driver/v5/neo4j"

	"example.org/depotwalk/internal/graph"
)

// Steps between two bins, walking along aisles. Bounded at 40 hops: the building is not that big.
const walk = `
MATCH p = SHORTEST 1 (a:Bin {code: $from})-[:NEXT_TO]-{1,40}(b:Bin {code: $to})
RETURN [n IN nodes(p) | n.code] AS bins, length(p) AS steps`

func Walk(ctx context.Context, driver neo4j.DriverWithContext, from, to string) ([]map[string]any, error) {
	return graph.Read(ctx, driver, walk, map[string]any{"from": from, "to": to})
}

// Order sorts a pick list greedily: always go to the nearest bin not yet visited.
func Order(start string, distance func(a, b string) int, picks []string) []string {
	remaining := append([]string(nil), picks...)
	ordered := make([]string, 0, len(picks))
	current := start
	for len(remaining) > 0 {
		best := 0
		for i := range remaining {
			if distance(current, remaining[i]) < distance(current, remaining[best]) {
				best = i
			}
		}
		current = remaining[best]
		ordered = append(ordered, current)
		remaining = append(remaining[:best], remaining[best+1:]...)
	}
	return ordered
}
