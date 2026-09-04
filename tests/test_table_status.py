"""Tests semantic status values in Clicycle tables."""

import io

import pytest
from rich.console import Console

import clicycle as cc
from clicycle.components.table import Table
from clicycle.theme import Icons, Theme, Typography


@pytest.mark.parametrize(
    ("status", "kind"),
    [
        (cc.Status.success("ready"), "success"),
        (cc.Status.warning("degraded"), "warning"),
        (cc.Status.error("failed"), "error"),
    ],
)
def test_status_factories(status: cc.Status, kind: str) -> None:
    assert status.kind == kind


def test_status_rejects_empty_message() -> None:
    with pytest.raises(ValueError, match="cannot be empty"):
        cc.Status.success("")


def test_status_rejects_unknown_kind() -> None:
    with pytest.raises(ValueError, match="Unknown table status kind"):
        cc.Status("message", "unknown")


def test_table_renders_status_with_configured_icon() -> None:
    theme = Theme(
        icons=Icons(success="YES"),
        typography=Typography(success_style="green", muted_style="dim"),
    )
    output = io.StringIO()
    console = Console(width=80, file=output, force_terminal=False)

    Table(
        theme,
        [{"Check": "Database", "Status": cc.Status.success("connected")}],
        show_header=False,
    ).render(console)

    assert "YES connected" in output.getvalue()


def test_table_renders_each_status_kind() -> None:
    theme = Theme()
    output = io.StringIO()
    console = Console(width=80, file=output, force_terminal=False)

    Table(
        theme,
        [
            {"Status": cc.Status.success("ready")},
            {"Status": cc.Status.warning("degraded")},
            {"Status": cc.Status.error("failed")},
        ],
        show_header=False,
    ).render(console)

    rendered = output.getvalue()
    assert f"{theme.icons.success} ready" in rendered
    assert f"{theme.icons.warning} degraded" in rendered
    assert f"{theme.icons.error} failed" in rendered
