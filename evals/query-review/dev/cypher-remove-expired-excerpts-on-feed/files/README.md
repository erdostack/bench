# syndic

The metadata graph Harrowgate Press syndicates to retailers: titles, the sample excerpts we license
to each retailer, and the retailers themselves.

    (:Title {isbn13})-[:HAS_EXCERPT]->(:Excerpt {excerptId, expiresOn})
    (:Retailer {code})-[:LICENSED {since}]->(:Excerpt)

- `bin/cy <target> "<cypher>"` or `bin/cy <target> --file <file>`: run Cypher on a target from
  `config/targets.toml` (cypher-shell underneath; password from `CY_<TARGET>_PASSWORD`).
- `changes/`: data changes, one file each, `YYYY-MM-DD-<what>.cypher`.
- `docs/ENVIRONMENTS.md`: the targets and how a change reaches each.
