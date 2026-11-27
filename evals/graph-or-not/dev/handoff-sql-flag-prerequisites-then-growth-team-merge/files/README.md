# flagship

Feature flags. The admin service stores flags in Postgres (`db/schema.sql`) and publishes a JSON snapshot
(`admin/snapshot.py`); every SDK downloads it and evaluates flags locally (`sdk/evaluate.js`).
