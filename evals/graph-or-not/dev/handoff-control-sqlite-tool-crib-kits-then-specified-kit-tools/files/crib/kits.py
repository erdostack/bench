"""Kit pages."""
from pathlib import Path

SQL = Path(__file__).resolve().parents[1] / "sql"


def run(conn, name, **params):
    return conn.execute((SQL / name).read_text(), params).fetchall()


def kit_page(conn, kit_id):
    top = run(conn, "kit_first_level.sql", kit_id=kit_id)
    # TODO: every tool in the kit, including tools in kits packed inside it
    return {"top": top}
