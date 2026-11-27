"""Kiosk screens. A tiny http.server app; the Pi has no web framework installed."""
import json
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Screens(BaseHTTPRequestHandler):
    def do_GET(self):
        conn = sqlite3.connect(ROOT / "var" / "kiosk.db")
        names = [n for (n,) in conn.execute("SELECT name FROM woman ORDER BY name")]
        conn.close()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({"women": names}).encode())


# TODO: "how is she connected to ..." screen: pick two women, show the chain of shared events between them.

if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 8000), Screens).serve_forever()
