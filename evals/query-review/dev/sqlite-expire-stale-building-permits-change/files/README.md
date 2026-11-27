# permitgraph

Building permits for the city's development services: permits, the parcels they are on, inspections and
appeals as rows in `node`, linked in `edge` (`db/schema.sql`, `docs/permits.md`). `var/permits.db` is the
dev copy; QA reviews changes there before they go to production.

- `changes/NNNN_<what>.sql`: data changes, applied in order with
  `python3 -c "import sqlite3,sys; c=sqlite3.connect('var/permits.db'); c.executescript(open(sys.argv[1]).read()); c.commit()" changes/<file>.sql`
