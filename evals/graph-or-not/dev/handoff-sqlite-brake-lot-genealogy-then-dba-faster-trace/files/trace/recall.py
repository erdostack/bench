"""Recall tracing for the quality team."""
from pathlib import Path

SQL = Path(__file__).resolve().parents[1] / "sql"


def containment(conn, lot_id):
    return conn.execute((SQL / "trace_forward.sql").read_text(), {"lot_id": lot_id}).fetchall()


def root_cause(conn, lot_id):
    return conn.execute((SQL / "trace_backward.sql").read_text(), {"lot_id": lot_id}).fetchall()

# TODO: the full-size traces are far too slow on production data; see the recall-tracing decision.
