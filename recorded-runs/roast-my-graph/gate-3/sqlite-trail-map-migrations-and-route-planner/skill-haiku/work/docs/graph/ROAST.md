# Roast: trailmap (migrations/, migrate.py, trailmap/, trails.db)

Verdict: Not sound. The live map already routes through closed junctions: 14 segments in trails.db point at junction ids that no longer exist, and route() walks through them. The README's claim that the planner can never send anyone through a closed junction does not hold.

Judged against:
- README.md: about 900 junctions and 1,400 segments; route() is a plain Dijkstra over all segments; close_junction is used when rangers close a bridge or junction; the README says foreign keys are on and close_junction removes touching segments.
- Live trails.db: 896 junctions, 1,388 segments, SQLite user_version 2.

## Findings

### critical: `segment`
Problem: Foreign keys are off on every connection the app opens. close_junction() leaves its segments behind. In the shipped trails.db, 14 segments reference missing junction ids 248, 433, 434 and 681, and route() passes through them (J1310 to J1426 goes through 433 and 434; J0009 to J1301 goes through 248).
Fix: Set PRAGMA foreign_keys = ON in connect_db() and anywhere else the database is opened. After a backup, run DELETE FROM segment WHERE from_junction NOT IN (SELECT id FROM junction) OR to_junction NOT IN (SELECT id FROM junction); once. Tested on a copy with SQLite 3.53.1: close_junction then leaves 0 dangling segments, and no sampled route passes a missing id.

### medium: `add_segment`
Problem: An unknown or closed junction code makes the INSERT ... SELECT insert zero rows, with no error. Tested: J9999 and the closed J0009 each added 0 rows silently.
Fix: Check cur.rowcount and raise ValueError when it is not 1.

### medium: `route`
Problem: An unknown or closed code raises KeyError, although the docstring promises None. Tested: KeyError 'J0009' and KeyError 'NOPE'.
Fix: Return None when either code is not in the junction table.

### low: `segment`
Problem: No UNIQUE constraint on (from_junction, to_junction). The shipped data has no duplicates, but nothing stops them.
Fix: Question to confirm whether parallel trails are intended. If not, add a unique index on (from_junction, to_junction) in a new migration.

### low: `PRAGMA foreign_keys`
Problem: The comment in migrations/001_init.sql says "for this database". The setting is per connection.
Fix: Reword the comment and point to connect_db().

## Holds up
- `segment` indexes `segment_from` and `segment_to`: they serve the cascade delete from close_junction() once foreign keys are on, and the referencing-column lookups that foreign key checks need. route() reads all segments with no filter, so these indexes do not speed it up.
- `segment` CHECK constraints (length_m > 0, difficulty and surface value sets, from_junction <> to_junction): they hold on the shipped data, and migration 002's ALTER TABLE with a default and CHECK is valid SQLite.
- `route` (Dijkstra with lazy deletion): correct for non-negative lengths, which the CHECK enforces. Reloading about 1,400 segments per call is cheap at this size.
- `migrate.py` with PRAGMA user_version: applies 001 and 002 in order on a fresh database (tested).

## Not checked
- The kiosk and web code that call close_junction are not in this repo, so how often closures happen was not confirmed.
- No timing was measured; judgement on speed rests on the README's sizes only.
- The one junction with no segments (J2416, id 737) was not treated as a defect; it may be intentional.
- Whether the live database was backed up is unknown; the cleanup was tested only on a copy.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
