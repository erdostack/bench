"""Character pages. Plain http.server."""
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Guide(BaseHTTPRequestHandler):
    def do_GET(self):
        conn = sqlite3.connect(ROOT / "var" / "guide.db")
        names = [n for (n,) in conn.execute("SELECT name FROM character ORDER BY name")]
        conn.close()
        self.send_response(200)
        self.end_headers()
        self.wfile.write("\n".join(names).encode())


# TODO: "closest companions" box on each character page: the characters this one shares the most chapters
# with, directly or through one other character.

if __name__ == "__main__":
    HTTPServer(("", 8000), Guide).serve_forever()
