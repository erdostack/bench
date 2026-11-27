# brightwork-stock

Stock graph of Brightwork Lighting Hire in Neo4j: every fixture we hire out, the kits they are packed
in, the stores they live in, and hires. The warehouse scanners, the hire desk and the workshop use it.

- `bin/lh <target> "<cypher>"` or `bin/lh <target> --file <file.cypher>`: send Cypher to a target in
  `config/targets.toml`.
- `changes/`: data changes, `NNNN-<what>.cypher`.
- `docs/`: environments, changes, the model, PAT testing.
