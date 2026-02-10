"""Spinner component with lifecycle management."""

from __future__ import annotations

from types import TracebackType
from typing import Literal

from rich.console import Console
from rich.live import Live
from rich.spinner import Spinner as RichSpinner
from rich.status import Status
from rich.table import Table

from clicycle.components.base import Component
from clicycle.theme import Theme


class Spinner(Component):
    """Animated spinner component for indicating ongoing operations.

    Shows an animated spinner with a message during long-running operations.
    Can be configured to disappear after completion (transient) or remain visible.
    Must be used as a context manager to manage lifecycle properly.

    Args:
        theme: Theme configuration including spinner type and disappearing behavior
        message: Status message to display alongside the spinner
        console: Rich console instance for rendering
        transient: Override theme's disappearing_spinners setting for this spinner

    Example:
        >>> import clicycle as cc
        >>> with cc.spinner("Loading data..."):
        ...     # Perform long operation
        ...     time.sleep(2)
        >>> # Spinner disappears after context exits (if transient=True or theme.disappearing_spinners=True)
    """

    component_type = "spinner"
    deferred_render = True  # Don't render immediately, wait for context manager

    def __init__(
        self,
        theme: Theme,
        message: str,
        console: Console,
        transient: bool | None = None,
    ):
        super().__init__(theme)
        self.message = message
        self.console = console
        self._context: Live | Status | None = None
        # Use explicit transient if provided, otherwise fall back to theme
        self._transient = (
            transient if transient is not None else theme.disappearing_spinners
        )
        self.was_transient = self._transient

    def get_spacing_before(self) -> int:
        """Get normal spacing - spinners should have normal spacing before them."""
        return super().get_spacing_before()

    def render(self, console: Console) -> None:
        """Render method - spinners start when context manager is entered."""
        # Don't start immediately, wait for context manager
        pass

    def __enter__(self) -> Spinner:
        """Start the spinner animation when entering context.

        Returns:
            Self for context manager usage
        """
        # Apply spacing BEFORE the spinner starts
        spacing = self.get_spacing_before()
        if spacing > 0:
            self.console.print("\n" * spacing, end="")

        if self._transient:
            # Create a grid table for spinner + text
            spinner = RichSpinner(
                self.theme.spinner_type, style=self.theme.typography.info_style
            )

            # Use Live display with transient for clean disappearing
            self._context = Live(
                spinner,
                console=self.console,
                transient=True,
                refresh_per_second=10,
            )
            # Update with actual content
            self._context.__enter__()

            # Create table with spinner and text
            table = Table.grid(padding=(0, 1))
            table.add_row(spinner, self.message)
            self._context.update(table)
        else:
            # Use regular status for persistent spinners
            self._context = self.console.status(
                self.message,
                spinner=self.theme.spinner_type,
                spinner_style=self.theme.typography.info_style,
            )
            self._context.__enter__()

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Literal[False]:
        """Stop the spinner animation when exiting context.

        Args:
            exc_type: Exception type if an error occurred
            exc_val: Exception value if an error occurred
            exc_tb: Exception traceback if an error occurred

        Returns:
            False to propagate any exceptions
        """
        if self._context:
            self._context.__exit__(exc_type, exc_val, exc_tb)

            # For non-disappearing spinners, print the final message
            if not self._transient:
                self.console.print(
                    f"[{self.theme.typography.info_style}]{self.message}[/]"
                )

        return False
