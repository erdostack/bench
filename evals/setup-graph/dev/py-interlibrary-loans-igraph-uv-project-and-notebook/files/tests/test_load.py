from illnet.load import network


def test_directed():
    assert network().is_directed()
