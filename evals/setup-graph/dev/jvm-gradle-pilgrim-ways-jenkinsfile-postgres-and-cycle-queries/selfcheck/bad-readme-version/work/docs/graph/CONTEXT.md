# Graph context

## Facts

engine: PostgreSQL
engine_version: 16
query_language: SQL
driver: org.postgresql:postgresql 42.7.4
run_queries: ./gradlew sql -Pfile=sql/route_options.sql
access: read-only
schema_snapshot: sql/schema.sql

## Evidence

- driver: gradle.lockfile (build.gradle.kts asks 42.7.+)
- run_queries: build.gradle.kts task sql -> org.waymarks.RunSql
- schema_snapshot: sql/schema.sql

## Open questions

- none
