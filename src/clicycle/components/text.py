"""Text-based components for displaying messages."""

from __future__ import annotations

from rich.console import Console

from clicycle.components.base import Component
from clicycle.theme import Theme


class Message(Component):
    """Base text component with automatic spacing and theming.

    The foundation for all text-based components. Handles message display with
    theme-based styling, icons, and automatic spacing between components.

    Args:
        theme: Theme configuration for styling and spacing
        message: Text content to display (must be non-empty string)
        text_type: Style variant - 'info', 'success', 'error', 'warning', or 'list_item'

    Raises:
        TypeError: If message is not a string
        ValueError: If message is empty

    Example:
        >>> from clicycle import Clicycle, Theme
        >>> cli = Clicycle()
        >>> text = Message(cli.theme, "Processing data...", "info")
    """

    def __init__(self, theme: Theme, message: str, text_type: str = "info"):
        super().__init__(theme)
        if not isinstance(message, str):
            raise TypeError(f"Message must be a string, got {type(message).__name__}")
        if not message:
            raise ValueError("Message cannot be empty")
        self.message = message
        self.text_type = text_type
        self.component_type = text_type  # For spacing rules

    def render(self, console: Console) -> None:
        """Render the text message with appropriate icon and style.

        Args:
            console: Rich console instance for rendering
        """
        icon_map = {
            "info": self.theme.icons.info,
            "success": self.theme.icons.success,
            "error": self.theme.icons.error,
            "warning": self.theme.icons.warning,
            "debug": self.theme.icons.debug,
        }

        style_map = {
            "info": self.theme.typography.info_style,
            "success": self.theme.typography.success_style,
            "error": self.theme.typography.error_style,
            "warning": self.theme.typography.warning_style,
            "debug": self.theme.typography.debug_style,
        }

        if self.text_type == "list_item":
            icon = self.theme.icons.bullet
            style = self.theme.typography.info_style
        else:
            icon = icon_map.get(self.text_type, self.theme.icons.info)
            style = style_map.get(self.text_type, self.theme.typography.info_style)

        # Get indentation for this text type
        indent_spaces = getattr(self.theme.indentation, self.text_type, 0)
        indent = " " * indent_spaces

        console.print(f"{indent}{icon} {self.message}", style=style)


class Info(Message):
    """Informational message component.

    Displays general information messages with standard styling.
    Typically used for status updates, instructions, or neutral information.

    Args:
        theme: Theme configuration for styling and spacing
        message: Information text to display

    Example:
        >>> import clicycle as cc
        >>> cc.info("Processing 1000 records...")
        >>> cc.info("Connected to database")
    """

    component_type = "info"

    def __init__(self, theme: Theme, message: str):
        super().__init__(theme, message, "info")


class Success(Message):
    """Success message component with checkmark icon.

    Displays success messages with green styling and a checkmark icon.
    Used to indicate successful operations, completions, or positive outcomes.

    Args:
        theme: Theme configuration for styling and spacing
        message: Success message to display (icon added automatically)

    Example:
        >>> import clicycle as cc
        >>> cc.success("Database migration completed")
        >>> cc.success("All tests passed")
    """

    component_type = "success"

    def __init__(self, theme: Theme, message: str):
        super().__init__(theme, message, "success")


class Error(Message):
    """Error message component with X icon.

    Displays error messages with red styling and an error icon.
    Used to indicate failures, errors, or problems that need attention.

    Args:
        theme: Theme configuration for styling and spacing
        message: Error message to display (icon added automatically)

    Example:
        >>> import clicycle as cc
        >>> cc.error("Failed to connect to server")
        >>> cc.error("Invalid configuration file")
    """

    component_type = "error"

    def __init__(self, theme: Theme, message: str):
        super().__init__(theme, message, "error")


class WarningText(Message):
    """Warning message component with warning icon.

    Displays warning messages with yellow/orange styling and a warning icon.
    Used for cautions, deprecations, or important notices that aren't errors.

    Args:
        theme: Theme configuration for styling and spacing
        message: Warning message to display (icon added automatically)

    Example:
        >>> import clicycle as cc
        >>> cc.warning("Deprecation: This feature will be removed in v4.0")
        >>> cc.warning("Low disk space available")
    """

    component_type = "warning"

    def __init__(self, theme: Theme, message: str):
        super().__init__(theme, message, "warning")


class ListItem(Message):
    """List item component with bullet point.

    Displays text as a list item with automatic bullet point and indentation.
    Multiple list items rendered consecutively create a formatted list.

    Args:
        theme: Theme configuration for styling and spacing
        message: List item text to display (bullet added automatically)

    Example:
        >>> import clicycle as cc
        >>> cc.list_item("First step: Install dependencies")
        >>> cc.list_item("Second step: Configure settings")
        >>> cc.list_item("Third step: Run the application")
    """

    component_type = "list_item"

    def __init__(self, theme: Theme, message: str):
        super().__init__(theme, message, "list_item")


class Text(Component):
    """Plain text component without icon.

    Displays text with the same styling as info but without the icon prefix.
    Useful for labels, headers within sections, or any text that doesn't need
    a status indicator.

    Args:
        theme: Theme configuration for styling and spacing
        message: Text content to display

    Example:
        >>> import clicycle as cc
        >>> cc.text("Remote")
        >>> cc.table(data)
    """

    component_type = "text"

    def __init__(self, theme: Theme, message: str):
        super().__init__(theme)
        if not isinstance(message, str):
            raise TypeError(f"Message must be a string, got {type(message).__name__}")
        if not message:
            raise ValueError("Message cannot be empty")
        self.message = message

    def render(self, console: Console) -> None:
        """Render the text message without icon.

        Args:
            console: Rich console instance for rendering
        """
        style = self.theme.typography.info_style
        indent_spaces = getattr(self.theme.indentation, "info", 0)
        indent = " " * indent_spaces
        console.print(f"{indent}{self.message}", style=style)
