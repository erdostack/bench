jobs/fix_ln388.py scales the 1,188 links that were last imported from cityroutes-v2 while importer 2.4.0 was
live (2026-10-02 08:00 to 2026-10-19 14:05 UTC). I went by the import time, not the size of the number: there are
cityroutes links of 12-35 m between sites across a footbridge and links of up to 39 km, so in kilometres and
metres the values overlap. Links imported before 2.4.0 went out (314) or since the fix (632) are already metres.
Batches of 400 (limit 500). It is not safe to run twice (it would multiply again), so run it once; afterwards
`SELECT count(*) FROM route_links WHERE source='cityroutes-v2' AND metres < 10` should be 0.
