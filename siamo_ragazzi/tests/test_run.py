import pytest
import click.testing
import siamo_ragazzi.__main__


@pytest.fixture()
def cli_runner():
    return click.testing.CliRunner()


class TestGeneration:
    def test_ragazzi(self, cli_runner: click.testing.CliRunner):
        result = cli_runner.invoke(siamo_ragazzi.__main__.main, args=[
            "-k", "i",
            "-t", "testiamo il software"
        ])
        assert not result.exception
