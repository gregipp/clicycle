"""Tests for the Divider component."""

from unittest.mock import MagicMock

from rich.console import Console

from clicycle.components.divider import Divider
from clicycle.theme import Layout, Theme


class TestDivider:
    """Test the Divider component."""

    def test_divider_basic(self):
        """Test basic divider rendering."""
        theme = Theme()
        console = MagicMock(spec=Console)

        divider = Divider(theme)
        divider.render(console)

        console.rule.assert_called_once_with(style="bright_black")

    def test_divider_uses_theme_style(self):
        """Test that divider uses theme's divider_style."""
        theme = Theme(layout=Layout(divider_style="cyan"))
        console = MagicMock(spec=Console)

        divider = Divider(theme)
        divider.render(console)

        console.rule.assert_called_once_with(style="cyan")

    def test_divider_component_type(self):
        """Test divider has correct component_type."""
        theme = Theme()
        divider = Divider(theme)
        assert divider.component_type == "divider"
