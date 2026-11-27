"""Profile page data."""
from pathlib import Path

SQL = Path(__file__).resolve().parents[1] / "sql"


def introductions(conn, viewer_id, member_id):
    """The badge: 1 (follows each other), 2 (friend of a friend) or None. Never looks further than 2."""
    if viewer_id == member_id:
        return None
    row = conn.execute((SQL / "introductions.sql").read_text(encoding="utf-8"),
                       {"viewer_id": viewer_id, "member_id": member_id}).fetchone()
    return row[0] if row else None


def profile(conn, viewer_id, member_id):
    handle, joined = conn.execute("SELECT handle, joined_on FROM member WHERE id = ?", (member_id,)).fetchone()
    followers = conn.execute("SELECT COUNT(*) FROM follow WHERE followed_id = ?", (member_id,)).fetchone()[0]
    return {"handle": handle, "joined": joined, "followers": followers,
            "introductions": introductions(conn, viewer_id, member_id)}
