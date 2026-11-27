import unittest

import networkx as nx

from lineage.graph import downstream_count, upstream


def small():
    G = nx.DiGraph()
    G.add_edges_from([("raw.orders", "stg.orders"), ("raw.customers", "stg.customers"), ("stg.orders", "mart.revenue"),
                      ("stg.customers", "mart.revenue"), ("stg.orders", "mart.basket"), ("raw.fx", "mart.revenue")])
    for n in G:
        G.nodes[n]["owner"] = "data-eng"
    return G


class Lineage(unittest.TestCase):
    def test_upstream(self):
        self.assertEqual(upstream(small(), "mart.revenue"),
                         ["raw.customers", "raw.fx", "raw.orders", "stg.customers", "stg.orders"])

    def test_upstream_of_source(self):
        self.assertEqual(upstream(small(), "raw.orders"), [])

    def test_downstream_count(self):
        self.assertEqual(downstream_count(small(), "stg.orders"), 2)


if __name__ == "__main__":
    unittest.main()
