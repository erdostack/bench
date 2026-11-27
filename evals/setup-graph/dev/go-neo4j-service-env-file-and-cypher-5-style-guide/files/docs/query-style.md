# Writing queries for watershed

- One query per file in `queries/`, parameters only, no string building in Go.
- We write Cypher 5, the language the server runs by default, so no `CYPHER` prefix is needed in the files.
- Variable-length patterns always get an upper bound (`*1..40` for river paths).
- Name relationship types in the direction water flows: `(:Reach)-[:FLOWS_INTO]->(:Reach)`.
- Return plain maps, not nodes, so `cmd/q` can print them as JSON lines.
