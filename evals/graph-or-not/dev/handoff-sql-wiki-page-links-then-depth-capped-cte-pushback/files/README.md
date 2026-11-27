# loreweb api

API behind the fandom wiki's reader features. Pages and links live in Postgres (`db/schema.sql`), loaded from the
wiki's nightly dump.

- `sql/`: queries the API runs (Postgres, positional parameters).
- `connect/`: the "how are these two pages connected" box (in progress).

The API runs on the app hosts (16 GB each), behind the CDN.
