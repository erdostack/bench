Trail map roast, done. Short version: the planner can route people through closed junctions, and the cause is a missing pragma in the connection code.

What I checked (on a copy of trails.db, live file untouched):

- Foreign keys are off for every connection the app opens. `connect_db()` never runs `PRAGMA foreign_keys = ON`, and the one in `001_init.sql` only applies to the migration's own connection. So `close_junction()` does not cascade. Closing a junction on a copy left all its segments in place.
- The live map already shows the damage. `PRAGMA foreign_key_check` reports 15 violating rows: 14 segments point at 4 deleted junction ids (248, 433, 434, 681).
- `route()` uses those orphaned segments. The fallback `codes.get(j, str(j))` prints the raw id as a junction code. Example on the copy: J0707 to J0907 comes back as 886 m via J0707, 248, J0907.
- `add_segment()` with an unknown code inserts zero rows and raises nothing. It also allows duplicate segments.
- `migrate()` commits each script before it bumps `user_version`, so a failed migration leaves a half-applied schema.
- `002_surface.sql` backfills 'dirt' onto all 1388 existing segments (723 now show 'dirt'), and `route()` never reads the column.
- The README says foreign keys make closed junctions unroutable. That is false as the code stands.

Fix order: turn on foreign keys in `connect_db()` and purge the orphans with a migration 003, then make `route()` ignore segments whose endpoints are gone and raise on unknown codes. After that, fix `add_segment()` to error on a bad code and make `close_junction()` delete its segments explicitly. Correct the README last.

Findings are in `findings.json` in the repo root, with 9 entries and severities from critical to low.
