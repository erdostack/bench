# treaty-exposure

Nightly exposure roll-up for group risk. Reads the treaty administration database (Postgres, `db/schema.sql`)
and writes exposure per reinsurer and contract to the risk mart.

- `exposure/rollup.sql`: the roll-up query.
- `jobs/nightly.sh`: runs it.
