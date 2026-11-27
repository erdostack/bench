# Degree audit: courses under a requirement

Decision: recursive-sql

## Workload facts (from the conversation of 2026-11-24)

- 1,900 requirements across 140 programmes, 14,000 course listings, nesting at most 5 levels.
- About 2,000 audit views a day in registration week, little otherwise. Catalogue rebuilt each term.
- The importer refuses a catalogue that is not a tree.

## Options considered

- graph-database (Kemal): rejected, a server for a once-a-term catalogue.
- recursive-sql: chosen, WITH RECURSIVE over parent_id.
- in-process-library: fine too at this size.

## What would change the decision

- Requirements that can share sub-requirements across programmes (no longer a tree), or per-student rules.
