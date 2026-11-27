import json
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from bylaws.impact import affected_by_repeal

ROOT = Path(__file__).resolve().parents[1]


class Site(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        conn = sqlite3.connect(ROOT / "var" / "register.db")
        if url.path == "/repeal-impact":
            bylaw = int(parse_qs(url.query)["id"][0])
            body = json.dumps(affected_by_repeal(conn, bylaw))
        else:
            body = json.dumps({"pages": ["/repeal-impact?id=N"]})
        conn.close()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(body.encode())


if __name__ == "__main__":
    HTTPServer(("", 8080), Site).serve_forever()
