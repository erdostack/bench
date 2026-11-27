# tallybook

Invoicing backend for a co-working space. A GraphQL API (Strawberry on FastAPI) over PostgreSQL.

    docker compose up -d db
    pip install -r requirements.txt
    make migrate
    make run          # http://localhost:8000/graphql

The GraphQL schema is in `app/schema.py`; the tables are in `migrations/`.
