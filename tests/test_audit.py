import importlib.util
import subprocess
from pathlib import Path

import pytest


@pytest.mark.parametrize("fail_lint", [False, True])
def test_audit_runs_both_packages_and_reports_failures(
    tmp_path, monkeypatch, capsys, fail_lint
):
    script = Path(__file__).resolve().parents[1] / "scripts" / "audit.py"
    spec = importlib.util.spec_from_file_location("local_audit", script)
    audit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(audit)
    monkeypatch.setattr(audit, "ROOT", tmp_path)

    for name in ("python-package", "django-package"):
        package = tmp_path / name
        (package / "src").mkdir(parents=True)
        (package / "pyproject.toml").touch()
    django = tmp_path / "django-package"
    (django / "manage.py").touch()
    (django / "tests").mkdir()
    (django / "tests" / "settings.py").touch()
    (django / "tests" / "test_example.py").touch()

    commands = []
    build_dirs = []

    def run(command, *, cwd, check):
        commands.append((command, cwd))
        if command[1:3] == ("-m", "build"):
            directory = Path(command[-1])
            build_dirs.append(directory)
            (directory / "package.whl").touch()
            (directory / "package.tar.gz").touch()
        status = int(fail_lint and command[1:4] == ("-m", "ruff", "check"))
        return subprocess.CompletedProcess(command, status)

    monkeypatch.setattr(audit.subprocess, "run", run)
    assert audit.main() == int(fail_lint)
    output = capsys.readouterr().out
    assert "WARNING: python-package: no Python tests found" in output
    assert any(
        command[1:3] == ("manage.py", "check") and cwd == django
        for command, cwd in commands
    )
    assert any(
        command[1:3] == ("-m", "pytest") and "--ds=tests.settings" in command
        for command, _ in commands
    )
    assert sum(command[1:3] == ("-m", "twine") for command, _ in commands) == 2
    assert sum(command[1:3] == ("-m", "xenon") for command, _ in commands) == 2
    assert len(build_dirs) == 2 and all(not path.exists() for path in build_dirs)
    if fail_lint:
        assert "FAILED: Ruff lint: exit 1" in output


def test_audit_rejects_missing_distributions(tmp_path, monkeypatch, capsys):
    script = Path(__file__).resolve().parents[1] / "scripts" / "audit.py"
    spec = importlib.util.spec_from_file_location("local_audit", script)
    audit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(audit)
    monkeypatch.setattr(audit, "ROOT", tmp_path)
    (tmp_path / "pyproject.toml").touch()
    (tmp_path / "src").mkdir()

    def run(command, *, cwd, check):
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(audit.subprocess, "run", run)
    assert audit.main() == 1
    output = capsys.readouterr().out
    assert "build produced no wheel" in output
    assert "build produced no source archive" in output
