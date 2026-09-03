"""Tests for the KeyValue component."""

import io
from unittest.mock import MagicMock

from rich.console import Console
from rich.table import Table as RichTable

from clicycle.components.key_value import KeyValue
from clicycle.theme import Theme


class TestKeyValue:
    """Test the KeyValue component."""

    def test_key_value_from_dict(self):
        """Test rendering key-value pairs from a dict."""
        theme = Theme()
        console = MagicMock(spec=Console)

        kv = KeyValue(theme, {"Status": "Online", "Uptime": "14d"})
        kv.render(console)

        console.print.assert_called_once()
        rendered = console.print.call_args[0][0]
        assert isinstance(rendered, RichTable)

    def test_key_value_from_list(self):
        """Test rendering key-value pairs from a list of tuples."""
        theme = Theme()
        console = MagicMock(spec=Console)

        kv = KeyValue(theme, [("Host", "prod-01"), ("Region", "us-east")])
        kv.render(console)

        console.print.assert_called_once()
        rendered = console.print.call_args[0][0]
        assert isinstance(rendered, RichTable)

    def test_key_value_with_title(self):
        """Test key-value with a title."""
        theme = Theme()
        console = MagicMock(spec=Console)

        kv = KeyValue(theme, {"a": "b"}, title="Server")
        kv.render(console)

        rendered = console.print.call_args[0][0]
        assert rendered.title == "Server"

    def test_key_value_empty(self):
        """Test empty data renders nothing."""
        theme = Theme()
        console = MagicMock(spec=Console)

        kv = KeyValue(theme, {})
        kv.render(console)

        console.print.assert_not_called()

    def test_key_value_borderless(self):
        """Test that the table has no box (borderless)."""
        theme = Theme()
        console = MagicMock(spec=Console)

        kv = KeyValue(theme, {"a": "b"})
        kv.render(console)

        rendered = console.print.call_args[0][0]
        assert rendered.box is None

    def test_key_value_long_value_folds(self):
        """A value wider than the console folds instead of being cut short."""
        theme = Theme()
        console = Console(width=30, file=io.StringIO(), force_terminal=False)

        KeyValue(
            theme, {"Context": "connectgateway_presyn-staging_global_stage"}
        ).render(console)

        output = console.file.getvalue()
        assert "…" not in output
        assert "".join(output.split()).endswith("global_stage")

    def test_key_value_component_type(self):
        """Test key_value has correct component_type."""
        theme = Theme()
        kv = KeyValue(theme, {"a": "b"})
        assert kv.component_type == "key_value"

    def test_key_value_non_string_values(self):
        """Test that non-string values are converted to strings."""
        theme = Theme()
        console = MagicMock(spec=Console)

        kv = KeyValue(theme, {"count": 42, "active": True, "rate": 3.14})
        kv.render(console)

        console.print.assert_called_once()
