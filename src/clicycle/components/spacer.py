"""Spacer component for explicit vertical whitespace."""

from __future__ import annotations

from rich.console import Console

from clicycle.components.base import Component
from clicycle.theme import Theme


class Spacer(Component):
    """Explicit vertical whitespace that bypasses automatic spacing.

    Renders a specified number of blank lines directly, without the
    automatic spacing system adding additional lines.

    Args:
        theme: Theme configuration
        lines: Number of blank lines to render (default: 1)

    Example:
        >>> import clicycle as cc
        >>> cc.spacer()       # 1 blank line
        >>> cc.spacer(3)      # 3 blank lines
    """

    component_type = "spacer"

    def __init__(self, theme: Theme, lines: int = 1):
        super().__init__(theme)
        self.lines = lines

    def get_spacing_before(self) -> int:
        """Spacer bypasses automatic spacing — always returns 0."""
        return 0

    def render(self, console: Console) -> None:
        """Render blank lines.

        Args:
            console: Rich console instance for rendering
        """
        for _ in range(self.lines):
            console.print()
