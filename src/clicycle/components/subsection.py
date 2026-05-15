"""Subsection component — a quieter header than ``cc.section``."""

from __future__ import annotations

from rich.console import Console

from clicycle.components.base import Component
from clicycle.theme import Theme


class Subsection(Component):
    """Subsection header — h2-level title with no full-width rule.

    ``cc.section`` renders a full-width horizontal rule with the title floated
    to the right, which is loud — appropriate for top-level groupings. When
    you need a quieter break inside a section (a sub-grouping, a step within
    a phase, etc.), ``cc.subsection`` prints just the title styled with the
    theme's ``subheader_style``. No rule, no indentation, no transform unless
    the theme asks for one.

    Args:
        theme: Theme configuration for styling and transforms.
        title: Subsection title text.

    Example:
        >>> import clicycle as cc
        >>> cc.section("Build")
        >>> cc.subsection("Compile")
        >>> cc.info("Compiling sources...")
        >>> cc.subsection("Link")
        >>> cc.info("Linking objects...")
    """

    component_type = "subsection"

    def __init__(self, theme: Theme, title: str):
        super().__init__(theme)
        self.title = title

    def render(self, console: Console) -> None:
        """Render the title styled as a subheader."""
        transformed = self.theme.transform_text(
            self.title,
            self.theme.typography.subheader_transform,
        )
        console.print(
            f"[{self.theme.typography.subheader_style}]{transformed}[/]",
        )
