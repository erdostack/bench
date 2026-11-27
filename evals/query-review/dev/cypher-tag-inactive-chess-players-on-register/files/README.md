# clubreg

The federation's membership register as a graph: players, clubs, and who belongs where. Neo4j 5.24
Enterprise, no plugins.

- `bin/reg register "<cypher>"` or `bin/reg register --file <file>`: run Cypher on the register.
- `changes/`: reviewed data changes, `<yyyy-mm-dd>-<what>.cypher`.
- `docs/register.md`: the database and how it is changed. `docs/model.md`: the model and property types.
