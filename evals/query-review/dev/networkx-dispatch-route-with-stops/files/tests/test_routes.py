import unittest

import networkx as nx

from linehaul.routes import fastest_route, runs_from


def small():
    G = nx.DiGraph()
    for a, b, m in [("AAL", "BRE", 50), ("BRE", "CPH", 40), ("AAL", "CPH", 120), ("CPH", "DUS", 30),
                    ("BRE", "DUS", 95), ("DUS", "AAL", 200), ("EIN", "AAL", 10)]:
        G.add_edge(a, b, minutes=m)
    for n in G:
        G.nodes[n]["region"] = "north"
    return G


class Routes(unittest.TestCase):
    def test_fastest(self):
        G = small()
        self.assertEqual(fastest_route(G, "AAL", "DUS"), 120)

    def test_unreachable(self):
        self.assertIsNone(fastest_route(small(), "AAL", "EIN"))

    def test_runs_from(self):
        self.assertEqual(runs_from(small(), "BRE"), [("CPH", 40), ("DUS", 95)])


if __name__ == "__main__":
    unittest.main()
