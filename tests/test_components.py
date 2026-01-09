"""Unit tests for clicycle components."""

from unittest.mock import MagicMock, patch

import pytest
from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table as RichTable

from clicycle.components.base import Component
from clicycle.components.code import Code
from clicycle.components.header import Header
from clicycle.components.section import Section
from clicycle.components.spinner import Spinner
from clicycle.components.table import Table
from clicycle.components.text import (
    Error,
    ListItem,
    Message,
    Success,
    Text,
    WarningText,
)
from clicycle.theme import Theme


class TestBaseComponent:
    """Test the base Component class."""

    def test_get_spacing_before_no_previous(self):
        """Test spacing calculation with no previous component."""
        theme = Theme()
        comp = Message(theme, "test", "info")
        comp.set_context(None)
        assert comp.get_spacing_before() == 0

    def test_get_spacing_before_with_rules(self):
        """Test spacing calculation with defined rules."""
        theme = Theme()
        theme.spacing.info = {"error": 2}

        prev_comp = Message(theme, "error", "error")
        comp = Message(theme, "info", "info")
        comp.set_context(prev_comp)

        assert comp.get_spacing_before() == 2

    def test_get_spacing_before_default(self):
        """Test default spacing when no rule defined."""
        theme = Theme()
        prev_comp = Message(theme, "test", "custom")
        comp = Message(theme, "info", "info")
        comp.set_context(prev_comp)

        assert comp.get_spacing_before() == 1

    def test_get_spacing_before_transient_reduction(self):
        """Test spacing reduction when previous component was transient."""
        theme = Theme()
        prev_comp = MagicMock()
        prev_comp.component_type = "spinner"
        prev_comp.was_transient = True

        comp = Message(theme, "info", "info")
        comp.set_context(prev_comp)
        # Default spacing is 1, reduced by 1 for transient = 0
        assert comp.get_spacing_before() == 0


class TestComponentBase:
    """Test the base Component class."""

    def test_deferred_render_skips_spacing(self):
        """Test that deferred components skip render_with_spacing."""

        # Create a test component with deferred_render attribute
        class DeferredComponent(Component):
            deferred_render = True
            component_type = "test"

            def render(self, console: Console) -> None:
                console.print("Should not be called")

        theme = Theme()
        console = MagicMock(spec=Console)

        component = DeferredComponent(theme)
        component.render_with_spacing(console)

        # Should return early and not call console.print
        console.print.assert_not_called()

    def test_abstract_render_method(self):
        """Test that render method is abstract."""
        theme = Theme()

        # Should not be able to instantiate Component directly
        with pytest.raises(TypeError):
            Component(theme)


class TestMessage:
    """Test the Message component (base text with icon)."""

    def test_message_render(self):
        """Test message component rendering."""
        theme = Theme()
        console = MagicMock(spec=Console)

        msg = Message(theme, "Hello", "info")
        msg.render(console)

        console.print.assert_called_once()
        call_args = console.print.call_args[0]
        assert "Hello" in str(call_args)

    def test_message_with_indentation(self):
        """Test message component with indentation."""
        theme = Theme()
        theme.indentation.info = 4
        console = MagicMock(spec=Console)

        msg = Message(theme, "Indented", "info")
        msg.render(console)

        console.print.assert_called_once()
        call_args = console.print.call_args[0]
        assert "    " in str(call_args)  # 4 spaces


class TestText:
    """Test the Text component (plain text without icon)."""

    def test_text_render(self):
        """Test plain text component rendering without icon."""
        theme = Theme()
        console = MagicMock(spec=Console)

        text = Text(theme, "Hello")
        text.render(console)

        console.print.assert_called_once()
        call_args = console.print.call_args[0][0]
        assert "Hello" in call_args
        # Should NOT contain the info icon
        assert theme.icons.info not in call_args

    def test_text_with_indentation(self):
        """Test plain text component with indentation."""
        theme = Theme()
        theme.indentation.info = 4
        console = MagicMock(spec=Console)

        text = Text(theme, "Indented")
        text.render(console)

        console.print.assert_called_once()
        call_args = console.print.call_args[0][0]
        assert "    " in call_args  # 4 spaces
        assert "Indented" in call_args

    def test_text_component_type(self):
        """Test that Text has correct component_type."""
        theme = Theme()
        text = Text(theme, "Test")
        assert text.component_type == "text"

    def test_text_validation(self):
        """Test Text validation for message."""
        theme = Theme()

        with pytest.raises(TypeError):
            Text(theme, 123)  # Not a string

        with pytest.raises(ValueError):
            Text(theme, "")  # Empty string


class TestTextComponents:
    """Test specific text component subclasses."""

    def test_success_component(self):
        """Test Success component initialization and rendering."""
        theme = Theme()
        console = MagicMock(spec=Console)

        success = Success(theme, "Operation successful")
        assert success.text_type == "success"
        assert success.component_type == "success"

        success.render(console)
        console.print.assert_called_once()
        call_args = console.print.call_args[0][0]
        assert theme.icons.success in call_args

    def test_error_component(self):
        """Test Error component initialization and rendering."""
        theme = Theme()
        console = MagicMock(spec=Console)

        error = Error(theme, "Something went wrong")
        assert error.text_type == "error"
        assert error.component_type == "error"

        error.render(console)
        console.print.assert_called_once()
        call_args = console.print.call_args[0][0]
        assert theme.icons.error in call_args

    def test_warning_component(self):
        """Test WarningText component initialization and rendering."""
        theme = Theme()
        console = MagicMock(spec=Console)

        warning = WarningText(theme, "Be careful")
        assert warning.text_type == "warning"
        assert warning.component_type == "warning"

        warning.render(console)
        console.print.assert_called_once()
        call_args = console.print.call_args[0][0]
        assert theme.icons.warning in call_args

    def test_list_item_component(self):
        """Test ListItem component initialization and rendering."""
        theme = Theme()
        console = MagicMock(spec=Console)

        item = ListItem(theme, "First item")
        assert item.text_type == "list_item"
        assert item.component_type == "list_item"

        item.render(console)
        console.print.assert_called_once()
        call_args = console.print.call_args[0][0]
        assert theme.icons.bullet in call_args


class TestHeader:
    """Test the Header component."""

    def test_header_basic(self):
        """Test basic header rendering."""
        theme = Theme()
        console = MagicMock(spec=Console)

        header = Header(theme, "Title")
        header.render(console)

        # Header calls print multiple times
        assert console.print.call_count >= 1

    def test_header_with_subtitle_and_app(self):
        """Test header with all fields."""
        theme = Theme()
        console = MagicMock(spec=Console)

        header = Header(theme, "Title", "Subtitle", "AppName")
        header.render(console)

        # Check that all parts were printed
        calls = [str(call) for call in console.print.call_args_list]
        all_calls = " ".join(calls)
        assert "TITLE" in all_calls  # Header converts to uppercase
        assert "Subtitle" in all_calls
        assert "AppName" in all_calls


class TestSection:
    """Test the Section component."""

    def test_section_render(self):
        """Test section rendering."""
        theme = Theme()
        console = MagicMock(spec=Console)

        section = Section(theme, "Section Title")
        section.render(console)

        # Section uses console.rule(), not print()
        console.rule.assert_called_once()
        call_args = console.rule.call_args
        # Check the actual call content
        assert "SECTION TITLE" in str(call_args)  # Title is transformed to uppercase


class TestListItemStyle:
    """Test list_item functionality through Message component."""

    def test_list_item_style(self):
        """Test that list items use the list style."""
        theme = Theme()
        console = MagicMock(spec=Console)

        # list_item creates a Message component with "list" style
        msg = Message(theme, "Item 1", "list")
        msg.render(console)

        console.print.assert_called_once()
        call_args = console.print.call_args[0]
        assert "Item 1" in str(call_args)

    def test_list_item_indentation(self):
        """Test list item indentation."""
        theme = Theme()
        theme.indentation.list = 6
        console = MagicMock(spec=Console)

        msg = Message(theme, "Indented item", "list")
        msg.render(console)

        console.print.assert_called_once()
        call_args = console.print.call_args[0]
        assert "      " in str(call_args)  # 6 spaces


class TestTable:
    """Test the Table component."""

    def test_table_render(self):
        """Test table rendering."""
        theme = Theme()
        console = MagicMock(spec=Console)

        data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
        table = Table(theme, data, title="Users")
        table.render(console)

        console.print.assert_called()
        # Should create a Rich Table
        call_args = console.print.call_args[0]
        assert isinstance(call_args[0], RichTable)

    def test_table_empty(self):
        """Test table with no data."""
        theme = Theme()
        console = MagicMock(spec=Console)

        table = Table(theme, [], title="Empty")
        table.render(console)

        # Empty table returns early and doesn't print anything
        console.print.assert_not_called()


class TestCode:
    """Test the Code component."""

    def test_code_render(self):
        """Test code rendering."""
        theme = Theme()
        console = MagicMock(spec=Console)

        code = Code(theme, "print('hello')", language="python", title="Example")
        code.render(console)

        console.print.assert_called()
        # Should create a Syntax object
        call_args = console.print.call_args[0]
        assert isinstance(call_args[0], Syntax)

    def test_code_with_line_numbers(self):
        """Test code with line numbers."""
        theme = Theme()
        console = MagicMock(spec=Console)

        code = Code(theme, "line1\nline2", language="text", line_numbers=True)
        code.render(console)

        console.print.assert_called()


class TestSpinner:
    """Test the Spinner component."""

    def test_spinner_context_manager(self):
        """Test spinner as context manager."""
        theme = Theme()
        console = MagicMock()
        console.is_jupyter = False
        console._live_stack = []
        console.set_live = MagicMock(return_value=True)
        console.set_alt_screen = MagicMock(return_value=False)
        console.show_cursor = MagicMock()
        console.push_render_hook = MagicMock()
        console.pop_render_hook = MagicMock()
        console.print = MagicMock()
        console.status = MagicMock()

        spinner = Spinner(theme, "Loading...", console)

        # Test context manager
        with spinner:
            assert spinner._context is not None

        # After exit, context should be cleaned up
        assert spinner._context is not None  # But reference remains

    def test_spinner_disappearing(self):
        """Test disappearing spinner mode."""
        theme = Theme(disappearing_spinners=True)
        console = MagicMock(spec=Console)

        spinner = Spinner(theme, "Loading...", console)
        assert spinner.was_transient is True

    def test_spinner_persistent(self):
        """Test persistent spinner mode."""
        theme = Theme(disappearing_spinners=False)
        console = MagicMock(spec=Console)

        spinner = Spinner(theme, "Loading...", console)
        assert spinner.was_transient is False

    @patch("clicycle.components.spinner.Live")
    def test_spinner_disappearing_live(self, mock_live):
        """Test disappearing spinner uses Live with transient."""
        theme = Theme(disappearing_spinners=True)
        console = MagicMock(spec=Console)

        spinner = Spinner(theme, "Loading...", console)
        mock_context = MagicMock()
        mock_live.return_value = mock_context

        with spinner:
            mock_live.assert_called_once()
            # Check that transient=True was passed
            call_kwargs = mock_live.call_args[1]
            assert call_kwargs["transient"] is True

    def test_spinner_persistent_status(self):
        """Test persistent spinner uses console.status."""
        theme = Theme(disappearing_spinners=False)
        console = MagicMock(spec=Console)
        mock_status = MagicMock()
        console.status.return_value = mock_status

        spinner = Spinner(theme, "Loading...", console)

        with spinner:
            console.status.assert_called_once_with(
                "Loading...",
                spinner=theme.spinner_type,
                spinner_style=theme.typography.info_style,
            )

    def test_spinner_transient_overrides_theme_false(self):
        """Test transient=True overrides theme's disappearing_spinners=False."""
        theme = Theme(disappearing_spinners=False)
        console = MagicMock(spec=Console)

        spinner = Spinner(theme, "Loading...", console, transient=True)
        assert spinner._transient is True
        assert spinner.was_transient is True

    def test_spinner_transient_overrides_theme_true(self):
        """Test transient=False overrides theme's disappearing_spinners=True."""
        theme = Theme(disappearing_spinners=True)
        console = MagicMock(spec=Console)

        spinner = Spinner(theme, "Loading...", console, transient=False)
        assert spinner._transient is False
        assert spinner.was_transient is False

    def test_spinner_transient_none_uses_theme(self):
        """Test transient=None (default) uses theme setting."""
        theme_true = Theme(disappearing_spinners=True)
        theme_false = Theme(disappearing_spinners=False)
        console = MagicMock(spec=Console)

        spinner_true = Spinner(theme_true, "Loading...", console)
        spinner_false = Spinner(theme_false, "Loading...", console)

        assert spinner_true._transient is True
        assert spinner_false._transient is False
