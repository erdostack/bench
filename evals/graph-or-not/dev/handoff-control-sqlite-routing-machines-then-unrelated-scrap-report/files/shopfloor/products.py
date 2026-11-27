"""Product page."""
from pathlib import Path

SQL = Path(__file__).resolve().parents[1] / "sql"


def run(conn, name, **params):
    return conn.execute((SQL / name).read_text(), params).fetchall()


def product_page(conn, product_id):
    routing = run(conn, "routing.sql", product_id=product_id)
    # TODO: the machines this product's routing uses
    return {"routing": routing}
