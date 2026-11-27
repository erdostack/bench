# Graph context

## Facts

engine: PostgreSQL
engine_version: 13.16
query_language: SQL (PostgreSQL 13)
driver: org.postgresql:postgresql 42.7.4
run_queries: ./gradlew sql -Pfile=sql/route_options.sql
access: read-only
schema_snapshot: sql/schema.sql

## Evidence

- engine_version: Jenkinsfile, docker.image('postgres:13.16')
- driver: gradle.lockfile (build.gradle.kts asks 42.7.+)
- run_queries: build.gradle.kts task sql -> org.waymarks.RunSql
- schema_snapshot: sql/schema.sql

## Open questions

- README.md says PostgreSQL 16; the Jenkinsfile starts postgres:13.16.
- Recursive CTEs with CYCLE detection are standard SQL:1999 and supported by PostgreSQL.
