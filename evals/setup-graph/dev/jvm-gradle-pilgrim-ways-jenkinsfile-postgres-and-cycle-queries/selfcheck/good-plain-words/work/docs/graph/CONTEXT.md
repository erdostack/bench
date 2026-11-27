# Graph context

## Facts

engine: postgres
engine_version: 13.16 (postgres:13.16 in the Jenkinsfile)
query_language: SQL
driver: postgresql 42.7.4 (pgjdbc)
run_queries: ./gradlew -q sql -Pfile=<file.sql>
access: read-only
schema_snapshot: sql/schema.sql

## Evidence

- engine_version: Jenkinsfile, docker.image('postgres:13.16')
- driver: gradle.lockfile (build.gradle.kts asks 42.7.+)
- run_queries: build.gradle.kts task sql -> org.waymarks.RunSql
- schema_snapshot: sql/schema.sql

## Open questions

- The README's PostgreSQL 16 is out of date.
