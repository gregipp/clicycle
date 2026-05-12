"""Verify clicycle re-exports the Rich primitives it wraps.

Callers should not need to import Rich directly to build a custom Table,
Panel, Group, or Live view alongside clicycle's component API.
"""

import rich.box
import rich.console
import rich.live
import rich.panel
import rich.table
import rich.text

import clicycle


class TestRichPrimitiveReexports:
    """Each Rich primitive used by clicycle's surface is re-exported."""

    def test_box_is_rich_box_class(self):
        assert clicycle.Box is rich.box.Box

    def test_group_is_rich_group(self):
        assert clicycle.Group is rich.console.Group

    def test_renderable_type_is_rich_renderable_type(self):
        assert clicycle.RenderableType is rich.console.RenderableType

    def test_live_is_rich_live(self):
        assert clicycle.Live is rich.live.Live

    def test_panel_is_rich_panel(self):
        assert clicycle.Panel is rich.panel.Panel

    def test_table_is_rich_table(self):
        assert clicycle.Table is rich.table.Table

    def test_text_is_rich_text(self):
        assert clicycle.Text is rich.text.Text


class TestBoxResolver:
    """clicycle.box() resolves a string name to a rich.box.Box."""

    def test_rounded(self):
        assert clicycle.box("rounded") is rich.box.ROUNDED

    def test_heavy_head(self):
        assert clicycle.box("heavy_head") is rich.box.HEAVY_HEAD

    def test_double(self):
        assert clicycle.box("double") is rich.box.DOUBLE
