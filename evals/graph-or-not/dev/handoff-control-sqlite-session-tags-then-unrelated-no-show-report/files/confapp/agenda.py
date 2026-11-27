"""Agenda pages."""
from pathlib import Path

SQL = Path(__file__).resolve().parents[1] / "sql"


def session_page(conn, session_id: int) -> dict:
    row = conn.execute((SQL / "session.sql").read_text(), {"session_id": session_id}).fetchone()
    if row is None:
        raise LookupError(session_id)
    title, room, starts_at = row
    # TODO: "related sessions" (programme committee)
    return {"title": title, "room": room, "starts_at": starts_at, "related": []}
