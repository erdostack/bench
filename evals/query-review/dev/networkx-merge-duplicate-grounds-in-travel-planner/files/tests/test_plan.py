from travel.graph import load_graph


def test_graph_loads():
    G = load_graph()
    assert G.number_of_nodes() > 100
    assert all("km" in d for _u, _v, d in G.edges(data=True))
