# trailmark

Data lineage for the analytics platform. A collector reads the warehouse's query log and records which
columns each job reads and writes; `lineage-api` answers "what is upstream of this?" and "what breaks
downstream if I change this?".

- `lineage-api`: Python 3.12, FastAPI (`lineage/`), deployed from `deploy/lineage-api.yaml`
- Store: PostgreSQL 16 (`db/schema.sql`)
- Clients: the web UI and `trailmark check`, a CI step that runs on every dbt pull request

Layout

    lineage/    API code
    db/         schema
    deploy/     Kubernetes manifests
    docs/       ADRs and requirements
    ops/        monthly exports
