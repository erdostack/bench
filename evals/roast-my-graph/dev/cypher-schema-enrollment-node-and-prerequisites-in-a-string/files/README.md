# coursegraph

Course catalogue and enrolments for the registrar's planning tools. Neo4j 5.

- `graph/schema.cypher`: constraints and indexes
- `graph/load.cypher`: nightly load from the student information system export; the loader passes `$rows`
- `graph/queries.cypher`: what the planner UI runs; each query has a `// name:` line

Size: about 48k students, 3.1k courses, 410k enrolments a year, six years kept.
