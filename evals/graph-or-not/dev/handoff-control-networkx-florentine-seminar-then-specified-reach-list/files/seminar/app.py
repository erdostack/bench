import sqlite3
from pathlib import Path

from flask import Flask, jsonify

DB = Path(__file__).resolve().parents[1] / "var" / "seminar.db"
app = Flask(__name__)


@app.get("/api/families")
def families():
    conn = sqlite3.connect(DB)
    try:
        return jsonify([f for (f,) in conn.execute("SELECT name FROM family ORDER BY name")])
    finally:
        conn.close()


# TODO: "reach" panel for the family pages
