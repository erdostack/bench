# registerlens

Explorer for the public company register: companies, the people who run and own them, and how they are
connected. Paying users are journalists, compliance teams and credit analysts.

- API: Python 3.12, FastAPI, psycopg 3 (`app/`)
- Database: PostgreSQL 16, one primary and two replicas
- Launched 2026-03-09

Layout

    app/        API handlers and SQL
    db/         schema
    docs/adr/   architecture decisions
    graph/      Neo4j migration (in progress, see ADR 0009)
    ops/        monthly exports from the API gateway and the database dashboard
    CHANGELOG.md
