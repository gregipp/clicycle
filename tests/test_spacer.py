"""Tests for the Spacer component."""

from unittest.mock import MagicMock, call

from rich.console import Console

from clicycle.components.spacer import Spacer
from clicycle.components.text import Message
from clicycle.theme import Theme


class TestSpacer:
    """Test the Spacer component."""

    def test_spacer_default_one_line(self):
        """Test spacer renders one blank line by default."""
        theme = Theme()
        console = MagicMock(spec=Console)

        spacer = Spacer(theme)
        spacer.render(console)

        console.print.assert_called_once_with()

    def test_spacer_multiple_lines(self):
        """Test spacer renders multiple blank lines."""
        theme = Theme()
        console = MagicMock(spec=Console)

        spacer = Spacer(theme, lines=3)
        spacer.render(console)

        assert console.print.call_count == 3
        console.print.assert_has_calls([call(), call(), call()])

    def test_spacer_bypasses_automatic_spacing(self):
        """Test that spacer always returns 0 for spacing_before."""
        theme = Theme()
        prev = Message(theme, "hello", "info")

        spacer = Spacer(theme)
        spacer.set_context(prev)

        assert spacer.get_spacing_before() == 0

    def test_spacer_bypasses_spacing_with_no_previous(self):
        """Test that spacer returns 0 even with no previous component."""
        theme = Theme()
        spacer = Spacer(theme)
        spacer.set_context(None)
        assert spacer.get_spacing_before() == 0

    def test_spacer_component_type(self):
        """Test spacer has correct component_type."""
        theme = Theme()
        spacer = Spacer(theme)
        assert spacer.component_type == "spacer"
