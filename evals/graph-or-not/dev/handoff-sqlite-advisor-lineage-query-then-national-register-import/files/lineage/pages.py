"""Tree page data."""
from pathlib import Path

SQL = Path(__file__).resolve().parents[1] / "sql"


def ancestors(conn, researcher_id):
    return conn.execute((SQL / "ancestors.sql").read_text(), {"researcher_id": researcher_id}).fetchall()
