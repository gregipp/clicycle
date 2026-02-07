"""Tests for the Panel component."""

from unittest.mock import MagicMock

from rich import box as rich_box
from rich.console import Console
from rich.panel import Panel as RichPanel

from clicycle.components.panel import Panel
from clicycle.theme import Layout, Theme


class TestPanel:
    """Test the Panel component."""

    def test_panel_basic(self):
        """Test basic panel rendering."""
        theme = Theme()
        console = MagicMock(spec=Console)

        panel = Panel(theme, "Hello world", title="Test")
        panel.render(console)

        console.print.assert_called_once()
        rendered = console.print.call_args[0][0]
        assert isinstance(rendered, RichPanel)

    def test_panel_with_subtitle(self):
        """Test panel with title and subtitle."""
        theme = Theme()
        console = MagicMock(spec=Console)

        panel = Panel(theme, "Content", title="Title", subtitle="Sub")
        panel.render(console)

        rendered = console.print.call_args[0][0]
        assert isinstance(rendered, RichPanel)
        assert rendered.title == "Title"
        assert rendered.subtitle == "Sub"

    def test_panel_uses_theme_box(self):
        """Test that panel uses the theme's panel_box setting."""
        theme = Theme(layout=Layout(panel_box=rich_box.DOUBLE))
        console = MagicMock(spec=Console)

        panel = Panel(theme, "Content")
        panel.render(console)

        rendered = console.print.call_args[0][0]
        assert rendered.box is rich_box.DOUBLE

    def test_panel_uses_theme_border_style(self):
        """Test that panel uses the theme's panel_border_style."""
        theme = Theme(layout=Layout(panel_border_style="cyan"))
        console = MagicMock(spec=Console)

        panel = Panel(theme, "Content")
        panel.render(console)

        rendered = console.print.call_args[0][0]
        assert rendered.border_style == "cyan"

    def test_panel_expand_defaults_to_theme(self):
        """Test that expand=None uses theme default."""
        theme = Theme(layout=Layout(panel_expand=False))

        panel = Panel(theme, "Content")
        assert panel.expand is False

    def test_panel_expand_override(self):
        """Test that explicit expand overrides theme."""
        theme = Theme(layout=Layout(panel_expand=True))

        panel = Panel(theme, "Content", expand=False)
        assert panel.expand is False

    def test_panel_component_type(self):
        """Test panel has correct component_type."""
        theme = Theme()
        panel = Panel(theme, "Content")
        assert panel.component_type == "panel"
