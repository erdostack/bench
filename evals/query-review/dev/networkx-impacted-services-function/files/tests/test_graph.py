import json
import tempfile
import unittest
from pathlib import Path

from svcmap.graph import load_graph, neighbours

SAMPLE = {"services": [{"name": n, "team": "t"} for n in ["web", "api", "db", "auth"]],
          "calls": [{"caller": "web", "callee": "api", "calls_per_min": 900},
                    {"caller": "api", "callee": "db", "calls_per_min": 2500},
                    {"caller": "api", "callee": "auth", "calls_per_min": 300}]}


class Neighbours(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        path = Path(self.tmp.name) / "calls.json"
        path.write_text(json.dumps(SAMPLE))
        self.G = load_graph(path)

    def tearDown(self):
        self.tmp.cleanup()

    def test_both_directions(self):
        self.assertEqual(neighbours(self.G, "api"), ["db", "web", "auth"])
        self.assertEqual(neighbours(self.G, "db"), ["api"])


if __name__ == "__main__":
    unittest.main()
