# glottonet

Language families as a graph (generated sample of a classification tree plus borrowing links), in Memgraph:
closest common ancestor of two languages, borrowing chains.

- Memgraph via compose.yaml; `make reset` reloads data/*.cypherl
- .NET 8 query tool in src/Glotto.Query
- The driver version is set once, in Directory.Build.props at the repo root (Neo4j.Driver 5.20.0)
- `make q F=queries/common_ancestor.cypher`
