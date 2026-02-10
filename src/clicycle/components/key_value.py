"""Key-value component for dashboard-style label:value displays."""

from __future__ import annotations

from rich.console import Console
from rich.table import Table as RichTable

from clicycle.components.base import Component
from clicycle.theme import Theme


class KeyValue(Component):
    """Dashboard-style key-value pair display using a borderless table.

    Renders aligned label:value pairs. Labels use the theme's label_style,
    values use the theme's value_style.

    Args:
        theme: Theme configuration for styling
        data: Key-value pairs as a dict or list of (key, value) tuples
        title: Optional title displayed above the pairs

    Example:
        >>> import clicycle as cc
        >>> cc.key_value({"Status": "Online", "Uptime": "14d 3h"})
        >>> cc.key_value([("Host", "prod-01"), ("Region", "us-east")], title="Server")
    """

    component_type = "key_value"

    def __init__(
        self,
        theme: Theme,
        data: dict[str, str | int | float | bool | None]
        | list[tuple[str, str | int | float | bool | None]],
        title: str | None = None,
    ):
        super().__init__(theme)
        self.data = data
        self.title = title

    def _iter_pairs(self) -> list[tuple[str, str]]:
        """Normalize data to a list of (key, string_value) pairs."""
        if isinstance(self.data, dict):
            return [(k, str(v)) for k, v in self.data.items()]
        return [(k, str(v)) for k, v in self.data]

    def render(self, console: Console) -> None:
        """Render key-value pairs as an aligned borderless table.

        Args:
            console: Rich console instance for rendering
        """
        pairs = self._iter_pairs()
        if not pairs:
            return

        table = RichTable(
            title=self.title,
            title_justify=self.theme.layout.title_align,
            box=None,
            show_header=False,
            padding=(0, 1),
            expand=False,
        )
        table.add_column(style=self.theme.typography.label_style)
        table.add_column(style=self.theme.typography.value_style)

        for key, value in pairs:
            table.add_row(key, value)

        console.print(table)
