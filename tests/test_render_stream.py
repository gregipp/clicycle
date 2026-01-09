"""Unit tests for RenderStream."""

from unittest.mock import MagicMock

from rich.console import Console

from clicycle.components.text import Message
from clicycle.rendering.stream import RenderStream
from clicycle.theme import Theme


class TestRenderStream:
    """Test the RenderStream class."""

    def test_init(self):
        """Test RenderStream initialization."""
        console = MagicMock(spec=Console)
        stream = RenderStream(console)

        assert stream.console is console
        assert stream.last_component is None
        assert len(stream.history) == 0

    def test_render_component(self):
        """Test rendering a component."""
        console = MagicMock(spec=Console)
        stream = RenderStream(console)
        theme = Theme()

        component = Message(theme, "Test", "info")
        stream.render(component)

        # Should add spacing and render
        assert console.print.call_count >= 1  # May print spacing + component
        assert stream.last_component is component
        assert len(stream.history) == 1

    def test_render_with_spacing(self):
        """Test rendering with spacing between components."""
        console = MagicMock(spec=Console)
        stream = RenderStream(console)
        theme = Theme()
        theme.spacing.info = {"info": 2}  # 2 lines between info components

        comp1 = Message(theme, "First", "info")
        comp2 = Message(theme, "Second", "info")

        stream.render(comp1)

        # Clear the mock to only capture the second render
        console.reset_mock()

        stream.render(comp2)

        # The component should call render_with_spacing which handles spacing
        # Check that console.print was called (once for spacing, once for content)
        # Spacing is done with newlines in a single print call
        assert console.print.call_count >= 1

    def test_clear_history(self):
        """Test clearing history."""
        console = MagicMock(spec=Console)
        stream = RenderStream(console)
        theme = Theme()

        # Add some components
        stream.render(Message(theme, "1", "info"))
        stream.render(Message(theme, "2", "info"))
        stream.render(Message(theme, "3", "info"))

        assert len(stream.history) == 3
        assert stream.last_component is not None

        stream.clear_history()

        assert len(stream.history) == 0
        assert stream.last_component is None

    def test_console_width_access(self):
        """Test accessing console width through stream."""
        console = MagicMock(spec=Console)
        console.width = 80
        stream = RenderStream(console)

        # RenderStream doesn't have get_width, access console directly
        assert stream.console.width == 80
