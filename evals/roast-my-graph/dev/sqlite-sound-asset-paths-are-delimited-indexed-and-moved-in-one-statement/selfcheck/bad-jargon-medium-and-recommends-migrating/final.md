It works for now, but the materialized path is a denormalised anti-pattern and GLOB is not sargable. I'd plan
the migration to an adjacency list with a closure table. Medium.
