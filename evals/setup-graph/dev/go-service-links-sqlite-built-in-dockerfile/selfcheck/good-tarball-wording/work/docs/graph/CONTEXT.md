# Graph context

## Facts

engine: SQLite (one file, data/stops.db)
engine_version: 3.46.1 (compiled from sqlite-autoconf-3460100 in the Dockerfile)
query_language: SQL (recursive CTEs over the link table)
driver: mattn/go-sqlite3 v1.14.24, built with -tags libsqlite3
run_queries: docker run --rm -v $(pwd):/work stopgraph:dev stopq -db data/stops.db -f queries/zone_crossings.sql
access: read-only
schema_snapshot: none

## Evidence

- engine: cmd/stopq/main.go opens data/stops.db with database/sql and the sqlite3 driver
- engine_version: Dockerfile builds libsqlite3 from sqlite-autoconf-3460100 (ARG SQLITE_VERSION=3.46.1) and the binary is built with -tags libsqlite3, so it links that library
- driver: go.mod requires github.com/mattn/go-sqlite3 v1.14.24
- run_queries: Makefile target q runs stopq inside the image
- access: stopq opens the file with mode=ro; nothing authorises writes

## Open questions

- Which SQLite? README.md: 3.40.1 from Debian. Dockerfile: its own build of 3.46.1, linked through -tags libsqlite3. The Dockerfile is what runs.
