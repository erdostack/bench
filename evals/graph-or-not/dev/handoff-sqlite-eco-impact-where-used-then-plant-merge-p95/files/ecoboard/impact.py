"""The ECO impact screen."""
from pathlib import Path

SQL = Path(__file__).resolve().parents[1] / "sql"


def where_used(conn, item_id):
    return conn.execute((SQL / "where_used.sql").read_text(), {"item_id": item_id}).fetchall()


def impact(conn, eco_id):
    (item_id,) = conn.execute("SELECT item_id FROM eco WHERE id = ?", (eco_id,)).fetchone()
    return [{"id": i, "part_no": p, "title": t, "level": lvl} for i, p, t, lvl in where_used(conn, item_id)]
