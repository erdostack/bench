# northlight-quotes

Quotes, hires and the stock list of Northlight Stage Hire, in Neo4j. The quoting tool, the hire desk and
invoicing all use it.

- `bin/nq <target> "<cypher>"` or `bin/nq <target> --file <file.cypher>`: send Cypher to a target in
  `config/targets.toml`.
- `changes/`: data changes, `YYYY-MM-DD-<ticket>-<what>.cypher`.
- `docs/`: where things run, how data is changed, the model, the quote rules.
