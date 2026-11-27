"""Flooding desk report: python -m drainage.desk <node_id>"""
import sqlite3
import sys

DB = "var/drainage.db"


def describe(conn, node_id):
    row = conn.execute("SELECT asset_ref, kind, catchment FROM node WHERE node_id = ?", (node_id,)).fetchone()
    if row is None:
        return f"node {node_id}: not in the export"
    return f"{row[0]} ({row[1]}, {row[2] or 'no catchment'})"


def main(argv):
    node_id = int(argv[1])
    conn = sqlite3.connect(DB)
    print("Flooded:", describe(conn, node_id))
    # TODO: list what drains into it (drainage/upstream.py, upstream_manholes(conn, node_id))
    conn.close()


if __name__ == "__main__":
    main(sys.argv)
