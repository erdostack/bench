"""The capacity planning run."""
from pathlib import Path

SQL = Path(__file__).resolve().parents[1] / "sql"


def changed_components(conn, run_id):
    return [r[0] for r in conn.execute("SELECT component_id FROM component_change WHERE run_id = ?", (run_id,))]


def where_used(conn, component_id):
    return [r[0] for r in conn.execute((SQL / "where_used.sql").read_text(), {"component_id": component_id})]


def run(conn, run_id, retime):
    for component_id in changed_components(conn, run_id):
        for assembly in where_used(conn, component_id):
            retime(assembly)
