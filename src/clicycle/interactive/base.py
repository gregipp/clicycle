"""Base classes for interactive components."""

from __future__ import annotations

import select as select_module
import sys
import termios
import tty
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from clicycle import Clicycle


class _BaseRenderer(ABC):
    """Base class for interactive renderers that use raw terminal IO."""

    def __init__(
        self, title: str, options: list[str | dict[str, Any]], cli: Clicycle
    ) -> None:
        self.title = title
        self.options = self._normalize_options(options)
        self.cli = cli
        self.current_index = 0
        self.selected_value: Any = None
        self.cursor_line = 0
        self.total_lines = 0

    def _normalize_options(
        self, options: list[str | dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Normalize options to a list of dictionaries."""
        return [
            {"label": opt, "value": opt} if isinstance(opt, str) else opt
            for opt in options
        ]

    def _get_key(self) -> str:
        """Read a single keypress, handling arrow keys and bare Escape."""
        key = sys.stdin.read(1)
        if key == "\x1b":
            # Wait briefly for arrow key sequence; bare ESC if nothing follows
            try:
                has_more = bool(select_module.select([sys.stdin], [], [], 0.05)[0])
            except (OSError, ValueError):
                has_more = True  # Assume arrow key in non-TTY contexts
            if has_more:
                key2 = sys.stdin.read(1)
                if key2 == "[":
                    key3 = sys.stdin.read(1)
                    if key3 == "A":
                        return "up"
                    if key3 == "B":
                        return "down"
            return "quit"
        if key in ("\r", "\n"):
            return "enter"
        if key == " ":
            return "space"
        if key in ("\x03", "q"):
            return "quit"
        return ""

    @abstractmethod
    def _setup_terminal(self) -> None:
        """Draw the initial menu and configure terminal."""
        raise NotImplementedError

    def _teardown_terminal(self, fd: int, old_settings: Any) -> None:
        """Restore terminal to its original state."""
        if self.cursor_line > 0:
            sys.stdout.write(f"\033[{self.cursor_line}A")

        for _ in range(self.total_lines):
            sys.stdout.write("\033[2K\033[B")

        if self.title:
            sys.stdout.write("\033[A\033[2K")

        sys.stdout.write(f"\033[{self.total_lines + bool(self.title)}A\r")
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        self.cli.console.show_cursor(True)

    @abstractmethod
    def _main_loop(self) -> None:
        """Handle user input and update display."""
        raise NotImplementedError

    def render(self) -> Any:
        """Render the select prompt and handle user input."""
        self._setup_terminal()
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            self._main_loop()
        finally:
            self._teardown_terminal(fd, old_settings)
        return self.selected_value
