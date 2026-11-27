"""Nightly: reset issue ids, then run group_crashes.sql until it updates no rows."""
from pathlib import Path

import psycopg

SQL = (Path(__file__).with_name("group_crashes.sql")).read_text()


def main(dsn):
    with psycopg.connect(dsn) as conn:
        conn.execute("UPDATE crash_report SET issue_id = id WHERE received_at > now() - interval '7 days'")
        while conn.execute(SQL).rowcount:
            pass
