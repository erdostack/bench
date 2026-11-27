# Changelog

## 0.9.0 (2025-05-12)

- upstream_path.sql and downstream_impact.sql now print each table's whole path, built with
  `string_agg(name, ' > ' ORDER BY depth)`. Ordered aggregate arguments and string_agg need SQLite 3.44.0
  or later.

## 0.8.0 (2024-06-03)

- Vendored dependencies (`go mod vendor`) so CI builds offline.

## 0.7.0 (2023-07-20)

- Moved from mattn/go-sqlite3 to modernc.org/sqlite: no cgo in the build any more.
