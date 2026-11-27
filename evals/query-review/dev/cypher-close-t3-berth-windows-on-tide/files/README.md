# berthplan

Berth planning for the port's container terminals as a Neo4j graph: terminals, berths, and the bookable
berth windows the shipping lines reserve for their calls. `docs/model.md` has the model.

- `bin/bp <target> "<cypher>"` / `bin/bp <target> --file <f>`: run Cypher on a target in `config/targets.toml`.
- `bin/migrate <target>`: apply pending migrations (release pipeline only).
- `migrations/`: schema and data migrations, `V<NNN>__<what>.cypher`.
- `docs/operations.md`: targets and how changes reach them.
