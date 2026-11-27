import sqlite3
from pathlib import Path

from flask import Flask, jsonify

ROOT = Path(__file__).resolve().parents[1]
app = Flask(__name__)


def db():
    return sqlite3.connect(ROOT / "var" / "inventory.db")


@app.get("/devices")
def devices():
    conn = db()
    rows = conn.execute("SELECT name, kind, room FROM device ORDER BY name").fetchall()
    conn.close()
    return jsonify([{"name": n, "kind": k, "room": r} for n, k, r in rows])


# TODO: transfer planner. Researchers pick two hosts and we tell them the rate a transfer between
# them can get.
