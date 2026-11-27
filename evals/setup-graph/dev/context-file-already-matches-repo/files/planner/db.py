import os

import psycopg


def connect() -> psycopg.Connection:
    conn = psycopg.connect(os.environ.get("PLANNER_DSN", "postgresql://planner@localhost:5432/planner"))
    conn.read_only = True
    return conn
