Added a partial unique index on (src, dst, kind, year) for ships_to and made the insert ON CONFLICT DO
NOTHING; it now walks all farms each run, so a crash anywhere is harmless.
