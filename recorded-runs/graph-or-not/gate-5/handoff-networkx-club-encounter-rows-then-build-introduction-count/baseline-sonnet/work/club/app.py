import sqlite3
from pathlib import Path

from flask import Flask, abort, jsonify

from club.graph import stats
from club.intro import introductions

DB = Path(__file__).resolve().parents[1] / "var" / "club.db"
app = Flask(__name__)


@app.get("/api/stats")
def club_stats():
    conn = sqlite3.connect(DB)
    try:
        return jsonify(stats(conn))
    finally:
        conn.close()


@app.get("/api/buddy-panel/<int:buddy>/<int:senior>")
def buddy_panel(buddy, senior):
    """Introductions from the newcomer's buddy to a senior member (null if the vouching ties don't connect them)."""
    conn = sqlite3.connect(DB)
    try:
        try:
            n = introductions(conn, buddy, senior)
        except KeyError:
            abort(404)
        return jsonify({"buddy": buddy, "senior": senior, "introductions": n})
    finally:
        conn.close()
