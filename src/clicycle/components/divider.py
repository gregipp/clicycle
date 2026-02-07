"""Divider component for subtle horizontal separators."""

from __future__ import annotations

from rich.console import Console

from clicycle.components.base import Component
from clicycle.theme import Theme


class Divider(Component):
    """Subtle horizontal rule for structural separation.

    A lightweight visual separator using the theme's divider_style.
    Distinct from Section, which is a prominent titled divider.

    Args:
        theme: Theme configuration for styling

    Example:
        >>> import clicycle as cc
        >>> cc.divider()
    """

    component_type = "divider"

    def __init__(self, theme: Theme):
        super().__init__(theme)

    def render(self, console: Console) -> None:
        """Render a horizontal rule.

        Args:
            console: Rich console instance for rendering
        """
        console.rule(style=self.theme.layout.divider_style)
