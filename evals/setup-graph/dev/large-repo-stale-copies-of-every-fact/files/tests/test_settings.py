from curio import settings


def test_reading_is_the_default():
    assert settings.Settings().access_mode == "READ"
