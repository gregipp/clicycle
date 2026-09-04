"""Table component for displaying structured data."""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Any

from rich import box as rich_box
from rich.console import Console
from rich.table import Table as RichTable
from rich.text import Text

from clicycle.components.base import Component
from clicycle.table_status import Status
from clicycle.theme import BoxName, Theme, _resolve_box

TableValue = str | int | float | bool | None | Status


class Table(Component):
    """Table component - displays data in tabular format.

    Args:
        theme: Theme configuration for styling
        data: List of dictionaries representing rows
        title: Optional table title
        column_widths: Optional dict mapping column names to widths
        wrap_text: Whether to wrap text or use ellipsis (default: True)
        no_wrap: Names of columns that never wrap. When the console is too
            narrow for every column, Rich shrinks the wrapping columns first,
            so identifiers (names, ids, hashes, ages) stay on one line and a
            prose column folds instead. A column listed here that still does
            not fit is cut with an ellipsis.
        expand: Whether to expand table to fill available width (default: False)
        width: Fixed width for the table (default: None, uses content width)
        page_size: Number of rows per page (None = no pagination)
        show_header: Whether to render the column-name header row (default: True)
        show_edge: Whether to render the box's top and bottom edges
            (default: True). ``False`` drops the blank or ruled lines that
            frame a ``"simple"`` table, for an aligned block with no frame.
        box: Per-call override for the table box style. Accepts a friendly
            ``BoxName`` (``"rounded"``, ``"simple"``, ...) or a ``rich.box.Box``.
            ``None`` falls back to ``theme.layout.table_box``.
    """

    component_type = "table"

    def __init__(
        self,
        theme: Theme,
        data: list[dict[str, TableValue]],
        title: str | None = None,
        column_widths: dict[str, int] | None = None,
        wrap_text: bool = True,
        no_wrap: Sequence[str] = (),
        expand: bool | None = None,
        width: int | None = None,
        page_size: int | None = None,
        show_header: bool = True,
        show_edge: bool = True,
        box: BoxName | rich_box.Box | None = None,
    ):
        super().__init__(theme)
        self.data = data
        self.title = title
        self.column_widths = column_widths or {}
        self.wrap_text = wrap_text
        self.no_wrap = frozenset(no_wrap)
        self.expand = expand if expand is not None else theme.layout.table_expand
        self.width = width
        self.page_size = page_size
        self.show_header = show_header
        self.show_edge = show_edge
        if box is None:
            self.box = theme.layout.table_box
        elif isinstance(box, str):
            self.box = _resolve_box(box)
        else:
            self.box = box

    def _build_table(self, rows: list[dict[str, TableValue]]) -> RichTable:
        """Build a Rich table from a slice of rows."""
        table = RichTable(
            title=self.title,
            title_justify=self.theme.layout.title_align,
            box=self.box,
            border_style=self.theme.layout.table_border_style,
            title_style=self.theme.typography.header_style,
            header_style=self.theme.typography.label_style,
            expand=self.expand,
            width=self.width,
            show_header=self.show_header,
            show_edge=self.show_edge,
        )

        columns = list(self.data[0].keys())
        for key in columns:
            column_name = str(key)
            col_width = self.column_widths.get(column_name)
            wraps = self.wrap_text and column_name not in self.no_wrap
            table.add_column(
                column_name,
                width=col_width,
                no_wrap=not wraps,
                overflow="fold" if wraps else "ellipsis",
            )

        for row in rows:
            table.add_row(*[self._render_cell(row.get(key, "")) for key in columns])

        return table

    def _render_cell(self, value: TableValue) -> str | Text:
        if isinstance(value, Status):
            return value.render(self.theme)
        return str(value)

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
