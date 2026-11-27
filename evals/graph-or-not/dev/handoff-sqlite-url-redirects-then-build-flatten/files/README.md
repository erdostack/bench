# shop-seo

Nightly jobs that keep the storefront's URLs in order.

- `shop/redirects.py` writes `deploy/redirects.map`, which nginx loads with a `map` block. It runs every night from
  cron on the jobs host.
- Production database: Postgres 16 (the catalogue database, read replica). Tests use SQLite built from
  `db/schema.sql`.
- Merchandisers create redirects in the CMS whenever a product URL changes; rows are never deleted.
