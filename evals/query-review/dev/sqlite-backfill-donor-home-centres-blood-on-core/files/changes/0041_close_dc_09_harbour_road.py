"""0041 (DS-310): Harbour Road (DC-09) closed on 2026-06-30. Its donors were asked to choose a new centre;
donor care set their home_centre by hand. This removes the home_centre edges still pointing at DC-09
for donors who were withdrawn before the closure.
Reviewed: p.lindqvist. Applied 2026-07-03."""


def run(conn):
    removed = 0
    while True:
        with conn:
            n = conn.execute(
                "DELETE FROM edges WHERE id IN (SELECT e.id FROM edges e JOIN nodes d ON d.id = e.src "
                "WHERE e.kind = 'home_centre' AND e.dst = (SELECT id FROM nodes WHERE code = 'DC-09') "
                "AND d.status = 'withdrawn' LIMIT 400)").rowcount
        if not n:
            return removed
        removed += n
