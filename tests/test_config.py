import importlib

import pytest


def test_default_configuration():
    import app.config.config as config

    assert config.CHUNK_SIZE > 0
    assert config.CHUNK_OVERLAP >= 0
    assert config.CHUNK_OVERLAP < config.CHUNK_SIZE


def test_invalid_chunk_size(monkeypatch):
    monkeypatch.setenv("CHUNK_SIZE", "0")

    import app.config.config as config

    with pytest.raises(ValueError, match="greater than zero"):
        importlib.reload(config)

    monkeypatch.delenv("CHUNK_SIZE", raising=False)
    importlib.reload(config)


def test_invalid_chunk_overlap(monkeypatch):
    monkeypatch.setenv("CHUNK_SIZE", "100")
    monkeypatch.setenv("CHUNK_OVERLAP", "100")

    import app.config.config as config

    with pytest.raises(ValueError, match="smaller than CHUNK_SIZE"):
        importlib.reload(config)

    monkeypatch.delenv("CHUNK_SIZE", raising=False)
    monkeypatch.delenv("CHUNK_OVERLAP", raising=False)
    importlib.reload(config)


def test_negative_chunk_overlap(monkeypatch):
    monkeypatch.setenv("CHUNK_SIZE", "100")
    monkeypatch.setenv("CHUNK_OVERLAP", "-1")

    import app.config.config as config

    with pytest.raises(
        ValueError,
        match="cannot be negative",
    ):
        importlib.reload(config)

    monkeypatch.delenv(
        "CHUNK_SIZE",
        raising=False,
    )
    monkeypatch.delenv(
        "CHUNK_OVERLAP",
        raising=False,
    )
    importlib.reload(config)
