"""Panel component for bordered content boxes."""

from __future__ import annotations

from rich import box as rich_box
from rich.console import Console, RenderableType
from rich.panel import Panel as RichPanel

from clicycle.components.base import Component
from clicycle.theme import BoxName, Theme, _resolve_box


class Panel(Component):
    """Bordered content box with optional title and subtitle.

    Wraps Rich Panel with theme integration for border style, box type,
    and expansion behavior.

    Args:
        theme: Theme configuration for styling
        content: Text or Rich renderable to display inside the panel
        title: Optional title displayed at the top border
        subtitle: Optional subtitle displayed at the bottom border
        expand: Whether to expand to fill width. None uses theme default.
        box: Per-call override for the panel box style. Accepts a friendly
            ``BoxName`` (``"rounded"``, ``"simple"``, ...) or a ``rich.box.Box``.
            ``None`` falls back to ``theme.layout.panel_box``.

    Example:
        >>> import clicycle as cc
        >>> cc.panel("System operational", title="Status")
        >>> cc.panel("Rate limit at 80%", title="Warning", subtitle="Updated 2m ago")
        >>> cc.panel("Quiet note", box="simple")
    """

    component_type = "panel"

    def __init__(
        self,
        theme: Theme,
        content: str | RenderableType,
        title: str | None = None,
        subtitle: str | None = None,
        expand: bool | None = None,
        box: BoxName | rich_box.Box | None = None,
    ):
        super().__init__(theme)
        self.content = content
        self.title = title
        self.subtitle = subtitle
        self.expand = expand if expand is not None else theme.layout.panel_expand
        if box is None:
            self.box = theme.layout.panel_box
        elif isinstance(box, str):
            self.box = _resolve_box(box)
        else:
            self.box = box

    def render(self, console: Console) -> None:
        """Render the panel with theme-configured styling.

        Args:
            console: Rich console instance for rendering
        """
        panel = RichPanel(
            self.content,
            title=self.title,
            title_align=self.theme.layout.title_align,
            subtitle=self.subtitle,
            subtitle_align="right",  # Subtitle stays right (e.g. timestamps)
            box=self.box,
            border_style=self.theme.layout.panel_border_style,
            expand=self.expand,
        )
        console.print(panel)
