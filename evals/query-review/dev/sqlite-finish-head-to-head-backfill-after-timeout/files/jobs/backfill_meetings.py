"""Backfill meetings from matches (docs/ranking.md): one winner -> loser edge per played match."""
import logging

BATCH = 500
log = logging.getLogger("backfill_meetings")


def run(conn):
    done, last_day, last_id = 0, "", 0
    while True:
        with conn:
            rows = conn.execute(
                "SELECT id, played_on FROM matches WHERE status = 'played' AND played_on < '2026-11-23' "
                "AND (played_on, id) > (?, ?) ORDER BY played_on, id LIMIT ?", (last_day, last_id, BATCH)).fetchall()
            if not rows:
                break
            conn.executemany(
                "INSERT INTO meetings (match_id, winner_id, loser_id, played_on) "
                "SELECT id, winner, CASE WHEN winner = p1 THEN p2 ELSE p1 END, played_on FROM matches WHERE id = ?",
                [(r[0],) for r in rows])
        done += len(rows)
        last_day, last_id = rows[-1][1], rows[-1][0]
        log.info("batch committed: %d meetings, through played_on %s", done, last_day)
    return done
