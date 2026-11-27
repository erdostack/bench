from accounts import store


def test_dsn_has_a_default():
    assert store.DSN.startswith("postgresql://")
