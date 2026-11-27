import sqlite3
from pathlib import Path

from flask import Flask, jsonify

DB = Path(__file__).resolve().parents[1] / "var" / "trails.db"
app = Flask(__name__)


@app.get("/api/junctions/<jid>")
def junction(jid):
    conn = sqlite3.connect(DB)
    try:
        row = conn.execute("SELECT id, name FROM junction WHERE id = ?", (jid,)).fetchone()
        segs = conn.execute("SELECT trail, junction_a, junction_b, length_m, minutes FROM segment "
                            "WHERE junction_a = ? OR junction_b = ?", (jid, jid)).fetchall()
        return jsonify({"junction": row, "segments": segs})
    finally:
        conn.close()


# TODO: /api/route?from=..&to=.. (fastest walking route)
