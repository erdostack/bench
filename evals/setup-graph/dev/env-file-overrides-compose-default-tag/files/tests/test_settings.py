from ferryboard.settings import Settings


def test_defaults():
    s = Settings()
    assert s.graph_user == "neo4j"
    assert s.min_transfer_minutes >= 0
