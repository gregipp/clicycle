"""Table component for displaying structured data."""

from __future__ import annotations

from rich.console import Console
from rich.table import Table as RichTable

from clicycle.components.base import Component
from clicycle.theme import Theme


class Table(Component):
    """Table component - displays data in tabular format."""

    component_type = "table"

    def __init__(
        self,
        theme: Theme,
        data: list[dict[str, str | int | float | bool | None]],
        title: str | None = None,
        column_widths: dict[str, int] | None = None,
        wrap_text: bool = True,
    ):
        super().__init__(theme)
        self.data = data
        self.title = title
        self.column_widths = column_widths or {}
        self.wrap_text = wrap_text

    def render(self, console: Console) -> None:
        """Render data as a table."""
        if not self.data:
            return

        table = RichTable(
            title=self.title,
            box=self.theme.layout.table_box,
            border_style=self.theme.layout.table_border_style,
            title_style=self.theme.typography.header_style,
            header_style=self.theme.typography.label_style,
        )

        # Add columns with optional width and configurable wrapping
        for key in self.data[0]:
            column_name = str(key)
            width = self.column_widths.get(column_name)
            table.add_column(
                column_name,
                width=width,
                no_wrap=not self.wrap_text,
                overflow="fold" if self.wrap_text else "ellipsis",
            )

        # Add rows
        for row in self.data:
            table.add_row(*[str(row.get(key, "")) for key in self.data[0]])

        console.print(table)
