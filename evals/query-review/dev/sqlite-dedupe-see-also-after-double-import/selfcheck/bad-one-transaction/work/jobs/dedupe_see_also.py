"""Remove rows of see_also that are exact repeats (the union import ran twice on 2026-11-14).

(a, b) and (b, a) are not duplicates: the OPAC looks suggestions up by `a`, so a two-way suggestion
needs both rows (docs/subjects.md)."""
CHUNK = 10 ** 6


def run(conn):
    doomed = [r for (r,) in conn.execute(
        """SELECT rowid FROM see_also s
           WHERE rowid > (SELECT min(rowid) FROM see_also t
                          WHERE t.a = s.a AND t.b = s.b AND t.added_by = s.added_by AND t.added_at = s.added_at)""")]
    for i in range(0, len(doomed), CHUNK):
        with conn:
            conn.executemany("DELETE FROM see_also WHERE rowid = ?", [(r,) for r in doomed[i:i + CHUNK]])
    return len(doomed)
