import sqlite3
from pathlib import Path

import networkx as nx
from flask import Flask, abort, jsonify

DB = Path(__file__).resolve().parents[1] / "var" / "seminar.db"
app = Flask(__name__)


@app.get("/api/families")
def families():
    conn = sqlite3.connect(DB)
    try:
        return jsonify([f for (f,) in conn.execute("SELECT name FROM family ORDER BY name")])
    finally:
        conn.close()


@app.get("/api/families/<name>/reach")
def reach(name):
    """Other families reachable through at most 1, 2 and 3 marriages, plus how many are exactly that far."""
    conn = sqlite3.connect(DB)
    try:
        if conn.execute("SELECT 1 FROM family WHERE name = ?", (name,)).fetchone() is None:
            abort(404)
        g = nx.Graph()
        g.add_nodes_from(f for (f,) in conn.execute("SELECT name FROM family"))
        g.add_edges_from(conn.execute("SELECT family_a, family_b FROM marriage_tie"))
    finally:
        conn.close()
    dist = nx.single_source_shortest_path_length(g, name, cutoff=3)
    exactly = {k: sum(1 for d in dist.values() if d == k) for k in (1, 2, 3)}
    within = {k: sum(exactly[j] for j in range(1, k + 1)) for k in (1, 2, 3)}
    return jsonify({"family": name, "within": within, "exactly": exactly})
