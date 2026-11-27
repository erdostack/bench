Saved sql/drop_retired_models.sql. docs/catalogue.md says a retired model is only removed once nothing refers
to it, and nothing in the database stops it: the FK on antennas.model_id isn't enforced (catalogue/db.py never
sets PRAGMA foreign_keys) and spares refer by code with no key at all. So the delete skips models still
installed or in spare stock. On var/catalogue.db it removes 25 of the 46 retired models; 21 stay (12 installed,
9 with spares). Check after: `SELECT count(*) FROM antennas a LEFT JOIN models m ON m.id = a.model_id WHERE m.id IS NULL` is 0.
