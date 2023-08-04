from typer.testing import CliRunner

from reportgen.cli import app

runner = CliRunner()


def test_search() -> None:
    result = runner.invoke(app, ["search", "93389150", "-d"])
    result_arg = runner.invoke(app, ["search", "93389150"])

    assert result.exit_code == 0
    assert result_arg.exit_code == 0


def test_version() -> None:
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
