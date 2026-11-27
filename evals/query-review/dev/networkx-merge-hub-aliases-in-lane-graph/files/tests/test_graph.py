import unittest

from lanenet.graph import load_aliases, load_graph


class GraphTest(unittest.TestCase):
    def test_loads(self):
        G = load_graph()
        self.assertGreater(G.number_of_edges(), 1000)
        self.assertTrue(set(load_aliases()) <= set(G))


if __name__ == "__main__":
    unittest.main()
