"""Semantic status values rendered by Clicycle tables."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Self

from rich.text import Text

from clicycle.theme import Theme

StatusKind = Literal["success", "warning", "error"]


@dataclass(frozen=True)
class Status:
    """A table-cell message with a semantic status."""

    message: str
    kind: StatusKind

    def __post_init__(self) -> None:
        if not isinstance(self.message, str):
            raise TypeError(
                f"Status message must be a string, got {type(self.message).__name__}"
            )
        if not self.message:
            raise ValueError("Status message cannot be empty")
        if self.kind not in ("success", "warning", "error"):
            raise ValueError(f"Unknown table status kind: {self.kind}")

    @classmethod
    def success(cls, message: str) -> Self:
        """Create a successful table status."""
        return cls(message=message, kind="success")

    @classmethod
    def warning(cls, message: str) -> Self:
        """Create a warning table status."""
        return cls(message=message, kind="warning")

    @classmethod
    def error(cls, message: str) -> Self:
        """Create an error table status."""
        return cls(message=message, kind="error")

    def render(self, theme: Theme) -> Text:
        """Render the configured icon and message styles."""
        icon = getattr(theme.icons, self.kind)
        status_style = getattr(theme.typography, f"{self.kind}_style")
        message_style = (
            theme.typography.muted_style if self.kind == "success" else status_style
        )
        return Text.assemble(
            (f"{icon} ", status_style),
            (self.message, message_style),
        )
