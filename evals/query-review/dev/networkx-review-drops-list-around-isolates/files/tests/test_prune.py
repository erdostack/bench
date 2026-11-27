import unittest

import networkx as nx

from jobs.prune import prune


class PruneTest(unittest.TestCase):
    def graph(self):
        G = nx.Graph()
        for n in ("p1", "p2"):
            G.add_node(n, kind="plant", last_seen="2024-05-01")
        for n in ("b1", "b2"):
            G.add_node(n, kind="pollinator", last_seen="2024-05-01")
        G.add_node("b3", kind="pollinator", last_seen="2009-07-12")
        G.add_edge("p1", "b1", seen="2010-06-01", visits=3)
        G.add_edge("p1", "b2", seen="2024-05-01", visits=1)
        G.add_edge("p2", "b1", seen="2023-08-11", visits=2)
        G.add_edge("p2", "b3", seen="2009-07-12", visits=1)
        return G

    def test_old_interactions_and_species_go(self):
        G = self.graph()
        self.assertEqual(prune(G, "2016-01-01"), (2, 1))
        self.assertEqual(sorted(G.edges), [("p1", "b2"), ("p2", "b1")])
        self.assertEqual(sorted(G.nodes), ["b1", "b2", "p1", "p2"])


if __name__ == "__main__":
    unittest.main()
