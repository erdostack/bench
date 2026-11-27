# Onboarding (first week)

Welcome. This page was written for the 0.9 release and is updated when someone trips over it.

## Day one

1. Clone the repository and create a virtualenv.
2. `pip install neo4j==5.14 fastapi uvicorn` is enough to run the API against the shared database.
3. Ask a maintainer for the shared database address and a read-only login.

## Running a query

    python tools/query.py queries/on_loan_now.cypher

The script prints a table. If it complains about authentication, your login has not been created yet.

## Reading list

- `docs/graph-model/overview.md` for the model.
- `docs/adr/` for why things are the way they are.
- The registrar's glossary (shared drive) for words like "accession" and "deaccession".
