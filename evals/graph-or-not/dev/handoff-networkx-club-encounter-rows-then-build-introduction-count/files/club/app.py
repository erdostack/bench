import sqlite3
from pathlib import Path

from flask import Flask, jsonify

from club.graph import stats

DB = Path(__file__).resolve().parents[1] / "var" / "club.db"
app = Flask(__name__)


@app.get("/api/stats")
def club_stats():
    conn = sqlite3.connect(DB)
    try:
        return jsonify(stats(conn))
    finally:
        conn.close()


# TODO: newcomer buddy panel: how many introductions from the newcomer's buddy to a senior member
