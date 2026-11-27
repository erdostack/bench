from clubnet.load import club_graph


def test_sizes():
    graph = club_graph()
    assert graph.number_of_nodes() == 34
    assert graph.number_of_edges() == 78
