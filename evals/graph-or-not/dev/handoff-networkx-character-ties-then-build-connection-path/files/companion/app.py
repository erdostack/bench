from flask import Flask, jsonify

from companion.db import connect
from companion.stats import most_connected

app = Flask(__name__)


@app.get("/api/most-connected")
def api_most_connected():
    conn = connect()
    try:
        return jsonify(most_connected(conn))
    finally:
        conn.close()


@app.get("/api/characters")
def api_characters():
    conn = connect()
    try:
        return jsonify([{"id": i, "name": n} for i, n in conn.execute("SELECT id, name FROM character ORDER BY name")])
    finally:
        conn.close()


# TODO: /api/connection?from=..&to=.. for the "how are these two connected" panel (editors' request)
