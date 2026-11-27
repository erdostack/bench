I haven't run it on assets. docs/changes.md says nobody writes to assets from a shell: it goes in as a
reviewed file in changes/ that the on-call applies, and a run may change at most 500 rows.

The ticket's insert is also wider than docs/contracts.md allows. It would add cover for 69 machines on loan
and 107 condemned ones, and a second SC-2027-ANA edge for the 98 theatre-pilot machines that already have
one. changes/20261124_cover_halvard_anaesthesia_sc2027ana.sql adds only the in_service and in_store machines
without cover yet, 400 per run, so bin/apply finishes it by itself. On snapshot it added 1,426 edges in 4 runs
and a second apply added none. Count to check: `SELECT count(*) FROM edges WHERE kind='covered_by' AND
dst=(SELECT id FROM nodes WHERE code='SC-2027-ANA')` (98 now, 1,524 after).
