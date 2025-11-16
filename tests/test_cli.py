"""Tests for the CLI and service entry points."""

import json
import os
from importlib import import_module, reload
from pathlib import Path

import pytest

from tictactoe.ui.cli import main as cli_main
from tictactoe.ui.service import main as service_main


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


def test_service_frontend_invoked(monkeypatch):
    service_module = import_module("tictactoe.ui.service.main")
    called = {"count": 0}

    def fake_main(argv=None):
        called["count"] += 1
        return 0

    monkeypatch.setattr(service_module, "main", fake_main)

    cli_module = _reload_cli_module()
    cli_module.main(["--ui", "service"])

    assert called["count"] == 1


def test_cli_list_frontends(capsys):
    cli_module = _reload_cli_module()
    result = cli_module.main(["--list-frontends"])

    captured = capsys.readouterr()
    assert "gui" in captured.out
    assert "cli" in captured.out
    assert "service" in captured.out
    assert result == 0


def test_cli_rejects_unknown_frontend(monkeypatch):
    monkeypatch.setenv("TICTACTOE_UI", "unknown")

    cli_module = _reload_cli_module()
    with pytest.raises(SystemExit) as excinfo:
        cli_module.main([])

    assert "Unknown frontend" in str(excinfo.value)


def test_cli_script_mode_emits_summary(tmp_path, capsys):
    outfile = tmp_path / "summary.json"
    cli_main.main(["--script", "0,3,4", "--output-json", str(outfile)])

    output = capsys.readouterr().out
    assert "Automation label" in output
    data = json.loads(outfile.read_text(encoding="utf-8"))
    assert data["metadata"]["action_count"] == "3"


def test_cli_script_invalid_move():
    with pytest.raises(SystemExit) as excinfo:
        cli_main.main(["--script", "0,9"])

    assert "Moves must be between" in str(excinfo.value)


def test_cli_script_file_argument(tmp_path, capsys):
    script_file = tmp_path / "moves.txt"
    script_file.write_text("1,2,3", encoding="utf-8")

    cli_main.main(["--script-file", str(script_file), "--label", "file-run"])

    output = capsys.readouterr().out
    assert "file-run" in output


def test_cli_script_quiet_suppresses_output(tmp_path, capsys):
    outfile = tmp_path / "summary.json"
    cli_main.main(["--script", "0,1", "--quiet", "--output-json", str(outfile)])

    assert capsys.readouterr().out.strip() == ""
    assert outfile.exists()


def test_cli_placeholder_message_when_no_args(capsys):
    cli_main.main([])
    output = capsys.readouterr().out
    assert "Template CLI placeholder" in output


def test_service_reads_environment(monkeypatch, tmp_path):
    monkeypatch.setenv("TICTACTOE_SCRIPT", "0,1")
    monkeypatch.setenv("TICTACTOE_AUTOMATION_OUTPUT", str(tmp_path / "svc.json"))
    monkeypatch.setenv("TICTACTOE_AUTOMATION_LABEL", "env-run")
    monkeypatch.setenv("TICTACTOE_AUTOMATION_QUIET", "0")

    service_main.main([])

    data = json.loads((tmp_path / "svc.json").read_text(encoding="utf-8"))
    assert data["label"] == "env-run"
    assert data["metadata"]["action_count"] == "2"


def test_service_warns_when_no_script(monkeypatch, capsys):
    monkeypatch.delenv("TICTACTOE_SCRIPT", raising=False)
    monkeypatch.delenv("TICTACTOE_SCRIPT_FILE", raising=False)

    service_main.main([])

    output = capsys.readouterr().out
    assert "No script provided" in output
