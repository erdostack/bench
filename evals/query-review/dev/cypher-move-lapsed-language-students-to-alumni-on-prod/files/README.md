# lingua-graph

Lingua House Language School's student graph in Neo4j 5.24: students, courses, teachers, the languages
taught and who is enrolled where. Bookings, the reception desk and the teachers' registers use it.

- `bin/lh <target> "<cypher>"` or `bin/lh <target> --file <file>`: run Cypher on a target in `config/targets.toml`.
- `changes/`: data changes, `V<nn>__<what>.cypher`. `docs/`: environment, changes, model.
