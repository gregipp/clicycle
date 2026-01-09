"""Tests for group component and context manager."""

from unittest.mock import MagicMock, mock_open, patch

from rich.console import Console

import clicycle as cc
from clicycle.clicycle import Clicycle
from clicycle.components.text import Message
from clicycle.modifiers.group import Group
from clicycle.theme import Theme


class TestGroup:
    """Test the Group component."""

    def test_group_init(self):
        """Test Group initialization."""
        theme = Theme()
        components = [
            Message(theme, "First", "info"),
            Message(theme, "Second", "success"),
        ]

        group = Group(theme, components)

        assert group.components == components
        assert group.component_type == "group"

    def test_group_render(self):
        """Test Group rendering."""
        theme = Theme()
        console = MagicMock(spec=Console)

        # Create mock components
        comp1 = MagicMock()
        comp2 = MagicMock()
        components = [comp1, comp2]

        group = Group(theme, components)
        group.render(console)

        # Should render each component
        comp1.render.assert_called_once_with(console)
        comp2.render.assert_called_once_with(console)

    @patch("builtins.open", new_callable=mock_open)
    def test_clicycle_group_context_manager(self, _mock_file):
        """Test Clicycle group context manager."""
        cli = Clicycle()

        # Mock components to be added to temp stream
        mock_component1 = MagicMock()
        mock_component2 = MagicMock()

        # Mock the original stream's render method
        original_stream = cli.stream
        original_stream.render = MagicMock()

        with patch("clicycle.clicycle.RenderStream") as mock_stream_class:
            # Set up mock stream to track history
            mock_temp_stream = MagicMock()
            mock_temp_stream.history = [mock_component1, mock_component2]
            mock_stream_class.return_value = mock_temp_stream

            with cli.group() as grouped_cli:
                # Inside the context, cli should have temporary stream
                assert grouped_cli is cli
                assert cli.stream is mock_temp_stream

        # After context, original stream should be restored
        assert cli.stream is original_stream

        # Should have rendered a Group with the components
        original_stream.render.assert_called_once()
        rendered_group = original_stream.render.call_args[0][0]
        assert isinstance(rendered_group, Group)
        assert rendered_group.components == [mock_component1, mock_component2]

    @patch("builtins.open", new_callable=mock_open)
    def test_clicycle_group_empty(self, _mock_file):
        """Test Clicycle group with no components."""
        cli = Clicycle()

        # Mock the original stream's render method
        original_stream = cli.stream
        original_stream.render = MagicMock()

        with patch("clicycle.clicycle.RenderStream") as mock_stream_class:
            # Set up mock stream with empty history
            mock_temp_stream = MagicMock()
            mock_temp_stream.history = []
            mock_stream_class.return_value = mock_temp_stream

            with cli.group():
                pass

        # Should not render anything if no components
        original_stream.render.assert_not_called()


class TestGroupIntegration:
    """Test group functionality through module interface."""

    def test_group_through_module_interface(self):
        """Test accessing group through module interface."""
        assert hasattr(cc, "group")
        assert callable(cc.group)

        # Should return the group context manager
        group_ctx = cc.group()
        assert hasattr(group_ctx, "__enter__")
        assert hasattr(group_ctx, "__exit__")
