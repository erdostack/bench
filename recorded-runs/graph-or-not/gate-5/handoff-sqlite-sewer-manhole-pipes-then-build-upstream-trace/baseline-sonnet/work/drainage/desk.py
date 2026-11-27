"""Flooding desk report: python -m drainage.desk <node_id>"""
import sqlite3
import sys

from drainage.upstream import upstream_manholes

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
    rows = upstream_manholes(conn, node_id)
    print(f"Drains into it ({len(rows)}, trace stops at pumping stations):")
    for _, ref, kind, catchment in rows:
        print(f"  {ref} ({kind}, {catchment or 'no catchment'})")
    conn.close()


if __name__ == "__main__":
    main(sys.argv)
