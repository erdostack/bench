"""Backfill meetings from matches (docs/ranking.md): one winner -> loser edge per played match.

Safe to kill and re-run: each batch picks played matches that have no meetings row yet, so rows written
by an earlier (killed) run are neither written again nor skipped."""
import logging

BATCH = 500
log = logging.getLogger("backfill_meetings")


def run(conn):
    with conn:
        conn.execute("CREATE INDEX IF NOT EXISTS meetings_match ON meetings (match_id)")
    done = 0
    while True:
        with conn:
            n = conn.execute(
                "INSERT INTO meetings (match_id, winner_id, loser_id, played_on) "
                "SELECT m.id, m.winner, CASE WHEN m.winner = m.p1 THEN m.p2 ELSE m.p1 END, m.played_on FROM matches m "
                "WHERE m.status = 'played' AND m.played_on < '2026-11-23' "
                "AND NOT EXISTS (SELECT 1 FROM meetings x WHERE x.match_id = m.id) "
                "ORDER BY m.played_on, m.id LIMIT ?", (BATCH,)).rowcount
        if not n:
            break
        done += n
        log.info("batch committed: %d meetings", done)
    return done
