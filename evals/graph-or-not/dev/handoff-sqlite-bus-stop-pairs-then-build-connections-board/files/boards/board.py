"""What one stop screen shows."""
from pathlib import Path

SQL = Path(__file__).resolve().parents[1] / "sql"


def query(name):
    return (SQL / f"{name}.sql").read_text(encoding="utf-8")


def board(conn, stop_id):
    stop = conn.execute("SELECT code, name FROM stop WHERE stop_id = ?", (stop_id,)).fetchone()
    here = conn.execute(query("routes_here"), {"stop_id": stop_id}).fetchall()
    return {
        "stop": {"code": stop[0], "name": stop[1]},
        "routes_here": [name for _, name in here],
        # TODO: "Connections" panel (sql/connections.sql)
        "connections": [],
    }
