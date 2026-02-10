"""Table component for displaying structured data."""

from __future__ import annotations

import math
from typing import Any

from rich.console import Console
from rich.table import Table as RichTable

from clicycle.components.base import Component
from clicycle.theme import Theme


class Table(Component):
    """Table component - displays data in tabular format.

    Args:
        theme: Theme configuration for styling
        data: List of dictionaries representing rows
        title: Optional table title
        column_widths: Optional dict mapping column names to widths
        wrap_text: Whether to wrap text or use ellipsis (default: True)
        expand: Whether to expand table to fill available width (default: False)
        width: Fixed width for the table (default: None, uses content width)
        page_size: Number of rows per page (None = no pagination)
    """

    component_type = "table"

    def __init__(
        self,
        theme: Theme,
        data: list[dict[str, str | int | float | bool | None]],
        title: str | None = None,
        column_widths: dict[str, int] | None = None,
        wrap_text: bool = True,
        expand: bool | None = None,
        width: int | None = None,
        page_size: int | None = None,
    ):
        super().__init__(theme)
        self.data = data
        self.title = title
        self.column_widths = column_widths or {}
        self.wrap_text = wrap_text
        self.expand = expand if expand is not None else theme.layout.table_expand
        self.width = width
        self.page_size = page_size

    def _build_table(
        self, rows: list[dict[str, str | int | float | bool | None]]
    ) -> RichTable:
        """Build a Rich table from a slice of rows."""
        table = RichTable(
            title=self.title,
            title_justify=self.theme.layout.title_align,
            box=self.theme.layout.table_box,
            border_style=self.theme.layout.table_border_style,
            title_style=self.theme.typography.header_style,
            header_style=self.theme.typography.label_style,
            expand=self.expand,
            width=self.width,
        )

        columns = list(self.data[0].keys())
        for key in columns:
            column_name = str(key)
            col_width = self.column_widths.get(column_name)
            table.add_column(
                column_name,
                width=col_width,
                no_wrap=not self.wrap_text,
                overflow="fold" if self.wrap_text else "ellipsis",
            )

        for row in rows:
            table.add_row(*[str(row.get(key, "")) for key in columns])

        return table

    def render(self, console: Console) -> None:
        """Render data as a table, with optional pagination."""
        if not self.data:
            return

        if self.page_size is None or len(self.data) <= self.page_size:
            console.print(self._build_table(self.data))
            return

        self._render_paginated(console)

    def _render_paginated(self, console: Console) -> None:
        """Render table with interactive page navigation."""
        from clicycle.interactive.select import interactive_select

        assert self.page_size is not None
        page_size = self.page_size
        total_pages = math.ceil(len(self.data) / page_size)
        current_page = 0

        while True:
            start = current_page * page_size
            end = start + page_size
            page_rows = self.data[start:end]

            console.print(self._build_table(page_rows))
            console.print(
                f"  Page {current_page + 1} of {total_pages} ({len(self.data)} items)",
                style="dim",
            )

            options: list[str | dict[str, Any]] = []
            if current_page < total_pages - 1:
                options.append({"label": "Next →", "value": "next"})
            if current_page > 0:
                options.append({"label": "← Previous", "value": "previous"})
            options.append({"label": "Done", "value": "done"})

            choice = interactive_select("", options)

            if choice == "next":
                current_page += 1
            elif choice == "previous":
                current_page -= 1
            else:
                break
