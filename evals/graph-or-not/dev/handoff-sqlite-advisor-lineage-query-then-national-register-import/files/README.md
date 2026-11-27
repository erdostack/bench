# lineage

The "academic family tree" pages for the graduate school: each researcher's advisors, their advisors, and so on
back, from the dissertation records.

- Python 3.12, SQLite (`var/lineage.db`, rebuilt nightly from the dissertation records by `lineage/build.py`, not
  committed). Tables in `db/schema.sql`.
- `sql/ancestors.sql` is the query behind the tree page.
