## Facts

engine: PostgreSQL
engine_version: 17.7
query_language: SQL
driver: psycopg[binary] 3.2.9 (via SQLAlchemy 2.0.41, URL scheme postgresql+psycopg)
run_queries: make psql
access: read-only
schema_snapshot: none

## Notes

- This repo has no graph database. It is a GraphQL API (Strawberry 0.270.1 on FastAPI) over a relational PostgreSQL database. GraphQL is the API layer, not the storage engine; the schema is in `app/schema.py`.
- Engine version comes from the `postgres:17.7` image in `docker-compose.yml`.
