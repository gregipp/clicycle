"""Tests for the main Clicycle class."""

import io
from unittest.mock import MagicMock

from rich.console import Console

from clicycle import Clicycle, Theme
from clicycle.rendering.stream import RenderStream


class TestClicycle:
    """Test the main Clicycle class."""

    def test_init_default(self):
        """Test Clicycle initialization with defaults."""
        cli = Clicycle()

        assert cli.width == 100
        assert isinstance(cli.theme, Theme)
        assert cli.app_name is None
        assert isinstance(cli.console, Console)
        assert isinstance(cli.stream, RenderStream)

    def test_init_custom_params(self):
        """Test Clicycle initialization with custom parameters."""
        custom_theme = Theme()
        cli = Clicycle(width=120, theme=custom_theme, app_name="TestApp")

        assert cli.width == 120
        assert cli.theme is custom_theme
        assert cli.app_name == "TestApp"
        # Note: cli.console.width is determined by terminal size, not the width parameter
        # The width parameter controls rendering behavior, not console dimensions

    def test_clear(self):
        """Test clear functionality."""
        cli = Clicycle()
        cli.console = MagicMock()
        cli.stream = MagicMock()

        cli.clear()

        cli.console.clear.assert_called_once()
        cli.stream.clear_history.assert_called_once()


class TestIndent:
    """Tests for ``Clicycle.indent`` context manager."""

    def _make_cli(self) -> tuple[Clicycle, io.StringIO]:
        """Build a Clicycle whose console writes to an in-memory buffer."""
        cli = Clicycle(width=40)
        buffer = io.StringIO()
        cli.console = Console(file=buffer, width=40, force_terminal=False)
        cli.stream = RenderStream(cli.console)
        return cli, buffer

    def test_indent_prefixes_each_line_with_spaces(self):
        """Every line printed inside the block has the indent prefix."""
        cli, buffer = self._make_cli()
        with cli.indent(4):
            cli.console.print("line one")
            cli.console.print("line two")
        out = buffer.getvalue()
        # Every non-empty rendered line starts with the 4-space prefix.
        for line in out.splitlines():
            if line:
                assert line.startswith("    ")

    def test_indent_zero_is_noop(self):
        """indent(0) yields without swapping the console."""
        cli, _ = self._make_cli()
        original_console = cli.console
        original_stream = cli.stream
        with cli.indent(0):
            assert cli.console is original_console
            assert cli.stream is original_stream
        assert cli.console is original_console

    def test_indent_negative_is_noop(self):
        """Negative indent is treated as 0."""
        cli, _ = self._make_cli()
        original_console = cli.console
        with cli.indent(-3):
            assert cli.console is original_console

    def test_indent_restores_console_after_block(self):
        """On exit, the original console and stream are reinstated."""
        cli, _ = self._make_cli()
        original_console = cli.console
        original_stream = cli.stream
        with cli.indent(2):
            assert cli.console is not original_console
            assert cli.stream is not original_stream
        assert cli.console is original_console
        assert cli.stream is original_stream

    def test_indent_restores_even_on_exception(self):
        """Console/stream are restored when the block raises."""
        cli, _ = self._make_cli()
        original_console = cli.console
        original_stream = cli.stream
        try:
            with cli.indent(2):
                raise RuntimeError("boom")
        except RuntimeError:
            pass
        assert cli.console is original_console
        assert cli.stream is original_stream

    def test_indent_nests(self):
        """An inner indent(2) inside an outer indent(2) totals 4 spaces."""
        cli, buffer = self._make_cli()
        with cli.indent(2), cli.indent(2):
            cli.console.print("deep")
        out = buffer.getvalue()
        deep_lines = [line for line in out.splitlines() if "deep" in line]
        assert deep_lines
        assert deep_lines[0].startswith("    ")
