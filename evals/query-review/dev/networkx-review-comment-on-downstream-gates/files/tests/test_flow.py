import unittest

import networkx as nx

from canalnet.flow import bottleneck, downstream, offtakes_below


def small():
    G = nx.DiGraph()
    for n, kind in [("H", "headworks"), ("A", "gate"), ("B", "gate"), ("C", "offtake"), ("D", "offtake")]:
        G.add_node(n, kind=kind)
    G.add_edge("H", "A", open=True, capacity=900)
    G.add_edge("A", "B", open=True, capacity=400)
    G.add_edge("A", "C", open=False, capacity=60)
    G.add_edge("B", "D", open=True, capacity=80)
    return G


class FlowTest(unittest.TestCase):
    def test_downstream_respects_closed_gates(self):
        self.assertEqual(downstream(small(), "H"), [("A", 1), ("B", 2), ("D", 3)])

    def test_offtakes(self):
        self.assertEqual(offtakes_below(small(), "A"), ["D"])

    def test_bottleneck(self):
        self.assertEqual(bottleneck(small(), ["H", "A", "B", "D"]), 80)


if __name__ == "__main__":
    unittest.main()
