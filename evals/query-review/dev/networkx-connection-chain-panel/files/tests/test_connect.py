import unittest

import networkx as nx

from people.connect import connection


class Connection(unittest.TestCase):
    def test_chain(self):
        G = nx.path_graph([1, 2, 3, 4])
        G.add_edge(1, 5)
        G.add_edge(5, 4)
        self.assertEqual(connection(G, 1, 4), [1, 5, 4])

    def test_too_far_or_apart(self):
        G = nx.path_graph(range(10))
        G.add_node(99)
        self.assertIsNone(connection(G, 0, 9, max_steps=6))
        self.assertIsNone(connection(G, 0, 99))
        self.assertEqual(connection(G, 0, 6), list(range(7)))


if __name__ == "__main__":
    unittest.main()
