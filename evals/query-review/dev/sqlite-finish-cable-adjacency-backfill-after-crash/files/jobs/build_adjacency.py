#!/usr/bin/env python3
"""Add one adjacency row (origin 'cable') per in-service cable, in batches of 50 cable ids, committing every
10 ids so the route planner's readers are never blocked for long.

Usage: build_adjacency.py <db> [--from-batch N]
"""
import argparse
import sqlite3
import sys
from datetime import datetime

BATCH = 50
COMMIT_EVERY = 10


def log(msg):
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S} {msg}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("db")
    ap.add_argument("--from-batch", type=int, default=1)
    a = ap.parse_args()
    conn = sqlite3.connect(a.db)
    top = conn.execute("SELECT max(id) FROM cables").fetchone()[0] or 0
    batches = (top + BATCH - 1) // BATCH
    for b in range(a.from_batch, batches + 1):
        lo, hi = (b - 1) * BATCH + 1, b * BATCH
        log(f"batch {b}/{batches}: cables {lo}-{hi}")
        for start in range(lo, hi + 1, COMMIT_EVERY):
            end = min(start + COMMIT_EVERY - 1, hi)
            conn.execute("INSERT INTO adjacency (src, dst, cable_id, origin) "
                         "SELECT a_site, b_site, id, 'cable' FROM cables "
                         "WHERE id BETWEEN ? AND ? AND status = 'in_service'", (start, end))
            conn.commit()
            log(f"  committed cables {start}-{end}")
    log("done")


if __name__ == "__main__":
    sys.exit(main())
