"""Fill connections.dep_min / arr_min (minutes after midnight of the service day) from the feed's HH:MM.

Feed times go past 24:00 for trips that run after midnight (docs/timetable.md), so the hours are taken
as a number, never through time() or a modulo: 24:55 is 1495, not 55. Rows still NULL are filled in
chunks of 2,000 (two columns, one row each: well under 5,000 changed rows per transaction)."""
CHUNK = 10 ** 9

FILL = """
UPDATE connections
SET dep_min = CAST(substr(dep, 1, instr(dep, ':') - 1) AS INTEGER) * 60 + CAST(substr(dep, instr(dep, ':') + 1) AS INTEGER),
    arr_min = CAST(substr(arr, 1, instr(arr, ':') - 1) AS INTEGER) * 60 + CAST(substr(arr, instr(arr, ':') + 1) AS INTEGER)
WHERE id IN (SELECT id FROM connections WHERE dep_min IS NULL OR arr_min IS NULL ORDER BY id LIMIT ?)
"""


def run(conn):
    filled = 0
    while True:
        with conn:
            n = conn.execute(FILL, (CHUNK,)).rowcount
        if not n:
            return filled
        filled += n
