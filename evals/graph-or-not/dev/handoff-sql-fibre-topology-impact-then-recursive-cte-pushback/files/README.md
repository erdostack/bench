# noc-impact

Backend for the NOC's impact screen: pick a fibre span or a device, see every customer-facing device that loses
service if it fails.

- Python 3.12, FastAPI, PostgreSQL 16 (the inventory database, shared with provisioning).
- `db/migrations/` is applied by the inventory team's migration runner; we only read.
- `uvicorn impact.api:app` for local work against a snapshot.
