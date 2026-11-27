"""Course pages. Plain http.server, the course VM has nothing else."""
import json
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]


def graph(conn):
    g = nx.Graph()
    g.add_nodes_from(i for (i,) in conn.execute("SELECT id FROM member"))
    g.add_edges_from(conn.execute("SELECT a, b FROM tie"))
    return g


class Pages(BaseHTTPRequestHandler):
    def do_GET(self):
        conn = sqlite3.connect(ROOT / "var" / "club.db")
        if self.path == "/degrees":
            body = json.dumps(dict(graph(conn).degree()))
        else:
            body = json.dumps({"pages": ["/degrees"]})
        conn.close()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(body.encode())


# TODO: "what would it take to split them" exercise: pick two members, show the cheapest split.

if __name__ == "__main__":
    HTTPServer(("", 8000), Pages).serve_forever()
