# Environments

## live

Production: the fault desk, the engineers' app and the customer status page. Data changes go in as a
reviewed file `changes/NNN-<what>.cypher` that the on-call runs, at most 5,000 rows per transaction.
Nobody writes to `live` by hand.

## dev

The developers' Neo4j 5.26 (no plugins, like live). It is disposable: `scripts/load-dev.sh` wipes it and rebuilds it from an
anonymised copy of last month's network plus whatever the fault simulator generates, and anyone can run
that at any time. Nothing outside the dev team reads it. Do what you like on `dev`, straight from
`bin/fq dev ...`: no change file, no review, no batch rule.

The fault simulator writes faults to `dev` with `simulated: true`. A rebuild loses any simulator run in
progress, so check with whoever started it before running `load-dev.sh`.
