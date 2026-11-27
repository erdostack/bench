import sqlite3
import sys


def run(conn, term):
    with conn:
        removed = conn.execute(
            "DELETE FROM edges WHERE rowid IN (SELECT e.rowid FROM edges e JOIN nodes l ON l.id = e.src "
            "WHERE e.kind = 'on_list' AND l.kind = 'list' AND l.term = ? AND coalesce(l.perpetual, 0) = 0 LIMIT 500)",
            (term,)).rowcount
    return removed


if __name__ == "__main__":
    print(run(sqlite3.connect("var/reslists.db"), sys.argv[1]))
