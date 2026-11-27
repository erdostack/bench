# curio

Collections database for a small museum consortium: objects, the people and workshops who made them, where each
object has been, and which objects are out on loan right now.

## Stack

- Python 3.12, FastAPI
- Neo4j 5.26.26 for the collection graph
- NetworkX for the offline "similar makers" job

## Quick start

    pip install -r requirements-dev.txt
    docker compose up -d
    ./scripts/run_query.sh queries/on_loan_now.cypher

The schema is documented in `db/schema.cypher`.

## Everyday work

See `CONTRIBUTING.md` for how we work and `docs/onboarding.md` for a longer walk-through. The examples under
`examples/quickstart` are the fastest way to see the API answer a question.
