"""Outage trace endpoint for the control-room client."""
from pathlib import Path

import psycopg

TRACE = (Path(__file__).resolve().parents[1] / "sql" / "outage_trace.sql").read_text(encoding="utf-8")


def still_fed(dsn, source_node, opened_segment):
    with psycopg.connect(dsn) as conn:
        rows = conn.execute(TRACE.replace(":source_node", "%(source_node)s").replace(":opened_segment", "%(opened_segment)s"),
                            {"source_node": source_node, "opened_segment": opened_segment}).fetchall()
    return {r[0] for r in rows}
