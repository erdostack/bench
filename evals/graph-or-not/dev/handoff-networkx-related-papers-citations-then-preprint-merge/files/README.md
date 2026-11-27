# scholar-api

API behind the research-discovery site: paper pages, search, and the "related papers" panel (papers
within three citation hops of the one you are reading, ranked by how many paths reach them). Papers and
citations are in Postgres (`db/schema.sql`), loaded nightly from the indexing pipeline.

- Python 3.12, `pip install -r requirements.txt`.
- Deployed as the `api` service (`deploy/api.yaml`).
