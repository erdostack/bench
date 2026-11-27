# Writing lineage queries

- The lineage database runs Cypher 5. Write Cypher 5 and keep to clauses it supports; do not use anything that
  only exists in Cypher 25.
- Always bound variable-length patterns (`*1..12`): some lines go back forty generations.
- Return accession codes, not internal ids.
- One query per file in `queries/`, with a comment saying what it answers.
