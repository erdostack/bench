# Graph context

## Facts

engine: sqlite
engine_version: 3.46.1
query_language: SQL (recursive CTEs over the link table)
driver: github.com/mattn/go-sqlite3 v1.14.24
run_queries: make q Q=queries/reachable_within.sql
access: read-only
schema_snapshot: sql/schema.sql

## Evidence

- engine: cmd/stopq/main.go opens data/stops.db with database/sql and the sqlite3 driver
- engine_version: Dockerfile builds libsqlite3 from sqlite-autoconf-3460100 (ARG SQLITE_VERSION=3.46.1) and the binary is built with -tags libsqlite3, so it links that library
- driver: go.mod requires github.com/mattn/go-sqlite3 v1.14.24
- run_queries: Makefile target q runs stopq inside the image
- access: stopq opens the file with mode=ro; nothing authorises writes

## Open questions

- README.md says the image uses Debian bookworm's SQLite 3.40.1. That is out of date: since the 2025-06-02 change the Dockerfile compiles SQLite 3.46.1 and links the binary against it. Recorded 3.46.1.
