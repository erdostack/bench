// Package load writes reaches and gauges from data/*.csv. Used by the nightly import job, not by people.
package load

import (
	"context"

	"github.com/neo4j/neo4j-go-driver/v5/neo4j"
)

func Reaches(ctx context.Context, d neo4j.DriverWithContext, rows []map[string]any) error {
	_, err := neo4j.ExecuteQuery(ctx, d,
		"UNWIND $rows AS r MERGE (a:Reach {id: r.id}) WITH a, r MATCH (b:Reach {id: r.into}) MERGE (a)-[:FLOWS_INTO]->(b)",
		map[string]any{"rows": rows}, neo4j.EagerResultTransformer)
	return err
}
