"""Tests for the CLI entry point."""

import os
from importlib import import_module, reload

import pytest

from tictactoe.ui.cli import main as cli_main


def _reload_cli_module():
    return reload(import_module("tictactoe.__main__"))


def test_cli_defaults_to_gui(monkeypatch):
    gui_module = import_module("tictactoe.ui.gui.main")
    called = {"count": 0}

    def fake_main():
        called["count"] += 1

    monkeypatch.setattr(gui_module, "main", fake_main)
    monkeypatch.delenv("TICTACTOE_UI", raising=False)

    cli_module = _reload_cli_module()
    result = cli_module.main([])

    assert called["count"] == 1
    assert result == 0


def test_cli_env_headless_sets_flag(monkeypatch):
    gui_module = import_module("tictactoe.ui.gui.main")
    called = {"headless": None}

    def fake_main():
        called["headless"] = os.environ.get("TICTACTOE_HEADLESS")

    monkeypatch.setattr(gui_module, "main", fake_main)
    monkeypatch.setenv("TICTACTOE_UI", "headless")
    monkeypatch.delenv("TICTACTOE_HEADLESS", raising=False)

    cli_module = _reload_cli_module()
    cli_module.main([])

    assert called["headless"] == "1"


def test_cli_flag_invokes_cli_frontend(monkeypatch):
    console_module = import_module("tictactoe.ui.cli.main")
    called = {"count": 0}

    def fake_main(argv=None):
        called["count"] += 1
        return 0

    monkeypatch.setattr(console_module, "main", fake_main)

    cli_module = _reload_cli_module()
    cli_module.main(["--ui", "cli"])

    assert called["count"] == 1


def test_cli_list_frontends(capsys):
    cli_module = _reload_cli_module()
    result = cli_module.main(["--list-frontends"])

    captured = capsys.readouterr()
    assert "gui" in captured.out
    assert "cli" in captured.out
    assert result == 0


def test_cli_rejects_unknown_frontend(monkeypatch):
    monkeypatch.setenv("TICTACTOE_UI", "unknown")

    cli_module = _reload_cli_module()
    with pytest.raises(SystemExit) as excinfo:
        cli_module.main([])

    assert "Unknown frontend" in str(excinfo.value)


def test_cli_script_mode_prints_board(capsys):
    result = cli_main.main(["--script", "0,3,4,6,8"])

    output = capsys.readouterr().out
    assert "Winner: X" in output
    assert "0 | 1 | 2" not in output  # board should show marks instead of index
    assert result == 0


def test_cli_script_invalid_move(monkeypatch):
    with pytest.raises(SystemExit) as excinfo:
        cli_main.main(["--script", "0,9"])

    assert "Moves must be between" in str(excinfo.value)


def test_cli_script_quiet_suppresses_output(capsys):
    cli_main.main(["--script", "0,3,4,6,8", "--quiet"])
    output = capsys.readouterr().out
    assert output.strip() == ""
