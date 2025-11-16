"""Tests for the configuration module."""

from importlib import import_module, reload


def test_config_exports_defined_all():
    config_module = reload(import_module("tictactoe.config"))
    assert isinstance(config_module.__all__, list)
    assert config_module.__all__ == []
