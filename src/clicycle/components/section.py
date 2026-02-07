"""Section component for dividing content."""

from __future__ import annotations

from rich.console import Console

from clicycle.components.base import Component
from clicycle.theme import Theme


class Section(Component):
    """Section divider component with horizontal rule.

    Creates a visual section break with a titled horizontal rule.
    Used to organize content into logical groups and improve readability.
    The title appears on the right side of the rule by default.

    Args:
        theme: Theme configuration for styling and spacing
        title: Section title text displayed with the rule

    Example:
        >>> import clicycle as cc
        >>> cc.section("Configuration")
        >>> cc.info("Setting up database connection...")
        >>> cc.section("Processing")
        >>> cc.info("Loading data files...")
    """

    component_type = "section"

    def __init__(self, theme: Theme, title: str):
        super().__init__(theme)
        self.title = title

    def render(self, console: Console) -> None:
        """Render section with horizontal rule and title.

        Args:
            console: Rich console instance for rendering
        """
        transformed_title = self.theme.transform_text(
            self.title,
            self.theme.typography.section_transform,
        )
        console.rule(
            f"[{self.theme.typography.section_style}]{transformed_title}[/]",
            style=self.theme.layout.divider_style,
            align="right",
        )
