I haven't run it on prod: docs/changes.md says nobody writes to prod by hand, changes go in as a reviewed
file the collections data manager applies with bin/apply. Two things about the insert as written: it adds
3,412 rows in one go (limit 400 per run), and bin/apply repeats a file until a run changes nothing, so it
would keep inserting the same edges forever.

changes/0041_backfill_off1_located_in.sql inserts 350 per run and skips objects that already have a
located_in edge, so it stops on its own and is safe to re-apply. On scratch: 3,412 edges added in 10 runs,
a second apply added nothing. Check with
`SELECT count(*) FROM nodes o WHERE o.location_code = 'OFF-1' AND NOT EXISTS (SELECT 1 FROM edges e WHERE e.src = o.id AND e.kind = 'located_in')`
(3,412 before, 0 after). After review: `bin/apply prod changes/0041_backfill_off1_located_in.sql`.
