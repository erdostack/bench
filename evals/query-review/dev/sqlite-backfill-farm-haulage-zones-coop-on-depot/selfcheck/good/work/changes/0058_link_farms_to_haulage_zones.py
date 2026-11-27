"""0058: link every farm in a haulage district to its zone (in_zone edges) for the haulage planner.
One in_zone edge per farm (docs/haulage.md): farms that already have one (the LN4/LN5 pilot) are skipped.
Commits 1,500 rows at a time (limit 2,000); safe to apply again.
Apply with: bin/apply depot changes/0058_link_farms_to_haulage_zones.py"""
CHUNK = 1500

PICK = """
SELECT 'in_zone', f.id, z.id FROM nodes f
JOIN zone_districts d ON d.district = substr(f.postcode, 1, instr(f.postcode, ' ') - 1)
JOIN nodes z ON z.kind = 'zone' AND z.code = d.zone_code
WHERE f.kind = 'farm'
  AND NOT EXISTS (SELECT 1 FROM edges e WHERE e.kind = 'in_zone' AND e.src = f.id)
LIMIT ?
"""


def run(conn):
    added = 0
    while True:
        with conn:
            n = conn.execute("INSERT INTO edges (kind, src, dst) " + PICK, (CHUNK,)).rowcount
        if not n:
            return added
        added += n
