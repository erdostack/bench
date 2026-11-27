"""Collections API: object pages."""
from pathlib import Path

SQL = Path(__file__).resolve().parent / "sql"


def related(conn, object_id):
    with conn.cursor() as cur:
        cur.execute((SQL / "related.sql").read_text().replace("$1", "%(id)s"), {"id": object_id})
        return cur.fetchall()
