"""Unified CLI theme configuration for Clicycle."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from rich import box as rich_box

TitleAlign = Literal["left", "center", "right"]


@dataclass
class Icons:
    """Icon configuration for CLI components.

    Defines the icons used throughout the CLI for various purposes.
    Uses Unicode symbols for broad terminal compatibility.

    Attributes:
        success: Checkmark for successful operations (✔)
        error: X mark for errors (✖)
        warning: Warning triangle for cautions (⚠)
        info: Information symbol (ℹ)
        running: Arrow for ongoing operations (→)
        bullet: Bullet point for lists (•)
    """

    # Core status icons
    success: str = "✔"
    error: str = "✖"
    warning: str = "⚠"
    info: str = "ℹ"

    # Progress and activity
    running: str = "→"
    waiting: str = "…"

    # Operations
    sync: str = "⟳"

    # Objects
    event: str = "◆"
    artist: str = "♪"
    image: str = "▣"
    url: str = "⎘"
    time: str = "◷"
    location: str = "◉"

    # Status indicators
    cached: str = "⚡"
    fresh: str = "✧"
    failed: str = "✖"
    debug: str = "›"

    # General
    bullet: str = "•"
    arrow_right: str = "→"
    arrow_left: str = "←"
    arrow_down: str = "↓"
    arrow_up: str = "↑"


@dataclass
class Typography:
    """Typography configuration for text styling.

    Controls colors, styles, and text transformations for all components.
    Uses Rich markup syntax for styling.

    Attributes:
        header_style: Style for main headers (default: "bold white")
        header_transform: Text transform for headers - "upper", "lower", "title", "none"
        success_style: Green styling for success messages
        error_style: Red styling for error messages
        warning_style: Yellow styling for warnings
        info_style: Cyan styling for info messages
    """

    # Headers
    header_style: str = "bold white"
    header_transform: str = "upper"  # upper, lower, title, none

    subheader_style: str = "dim white"
    subheader_transform: str = "none"

    # Sections
    section_style: str = "bold bright_blue"
    section_transform: str = "upper"
    section_underline: str = "─"  # Character to repeat for underline

    # Labels and values
    label_style: str = "bold"
    value_style: str = "default"

    # Status messages
    success_style: str = "bold green"
    error_style: str = "bold red"
    warning_style: str = "bold yellow"
    info_style: str = "cyan"
    debug_style: str = "dim cyan"

    # Other text
    muted_style: str = "bright_black"
    dim_style: str = "dim"


@dataclass
class Layout:
    """Layout configuration."""

    # Global
    title_align: TitleAlign = "left"

    # Table
    table_box: rich_box.Box = field(default_factory=lambda: rich_box.HEAVY_HEAD)
    table_border_style: str = "bright_black"
    table_expand: bool = True

    # Panel
    panel_box: rich_box.Box = field(default_factory=lambda: rich_box.ROUNDED)
    panel_border_style: str = "bright_black"
    panel_expand: bool = True

    # Divider
    divider_style: str = "bright_black"

    # URL display
    url_style: str = "full"  # "full", "domain", "compact"


@dataclass
class ComponentSpacing:
    """Spacing rules between consecutive components.

    Defines how many blank lines appear between different component types.
    Default spacing is 1 line. Only exceptions need to be specified.
    Uses a dictionary mapping previous component type to spacing.

    Example:
        info: {"info": 0}  # No spacing between consecutive info messages
        list_item: {"list_item": 0}  # No spacing between list items
    """

    info: dict[str, int] = field(default_factory=lambda: {"info": 0})
    debug: dict[str, int] = field(default_factory=lambda: {"debug": 0})
    code: dict[str, int] = field(
        default_factory=lambda: {
            "info": 0,
            "code": 0,
        }
    )
    list_item: dict[str, int] = field(
        default_factory=lambda: {
            "info": 0,
            "debug": 0,
            "list_item": 0,
        }
    )
    panel: dict[str, int] = field(default_factory=dict)
    key_value: dict[str, int] = field(default_factory=dict)
    divider: dict[str, int] = field(
        default_factory=lambda: {
            "divider": 0,
        }
    )


@dataclass
class ComponentIndentation:
    """Indentation configuration for text components.

    Controls the number of spaces used to indent different text types.
    Useful for creating visual hierarchy in output.

    Attributes:
        info: Spaces before info messages (default: 0)
        list_item: Spaces before list items (default: 2)
    """

    info: int = 0
    success: int = 0
    error: int = 0
    warning: int = 0
    debug: int = 0
    list_item: int = 2  # list_item defaults to two spaces


@dataclass
class Theme:
    """Complete theme configuration for Clicycle.

    The central configuration object that controls all visual aspects
    of the CLI output including colors, spacing, icons, and behavior.

    Args:
        icons: Icon set configuration
        typography: Text styling configuration
        layout: Layout configuration for tables and display
        spacing: Rules for spacing between components
        indentation: Rules for component indentation
        width: Console width in characters (must be >= 20)
        disappearing_spinners: Whether spinners vanish after completion
        spinner_type: Animation style ("dots", "line", "bouncingBar", etc.)

    Raises:
        ValueError: If width < 20 or invalid spinner_type

    Example:
        >>> from clicycle import Theme
        >>> theme = Theme(
        ...     width=120,
        ...     disappearing_spinners=True,
        ...     spinner_type="dots2"
        ... )
    """

    icons: Icons = field(default_factory=Icons)
    typography: Typography = field(default_factory=Typography)
    layout: Layout = field(default_factory=Layout)
    spacing: ComponentSpacing = field(default_factory=ComponentSpacing)
    indentation: ComponentIndentation = field(default_factory=ComponentIndentation)

    # Layout basics
    width: int = 100
    indent: str = "  "

    # Spinner behavior
    disappearing_spinners: bool = False
    spinner_type: str = (
        "dots"  # Rich spinner types: dots, dots2, dots3, line, bouncingBar, etc.
    )

    # Performance optimization: cached formatted styles
    _style_cache: dict[str, str] = field(default_factory=dict, init=False, repr=False)

    def __post_init__(self) -> None:
        """Validate theme and pre-compute cached styles."""
        # Validate width
        if not isinstance(self.width, int) or self.width < 20:
            raise ValueError(f"Width must be an integer >= 20, got {self.width}")

        # Validate spinner type
        valid_spinners = {
            "dots",
            "dots2",
            "dots3",
            "line",
            "star",
            "bouncingBar",
            "arc",
            "arrow",
        }
        if self.spinner_type not in valid_spinners:
            raise ValueError(
                f"Invalid spinner type '{self.spinner_type}'. Must be one of: {', '.join(valid_spinners)}"
            )

        # Pre-compute and cache frequently used style combinations
        self._style_cache.update(
            {
                "info_icon": f"{self.icons.info} ",
                "success_icon": f"{self.icons.success} ",
                "warning_icon": f"{self.icons.warning} ",
                "error_icon": f"{self.icons.error} ",
                "debug_icon": f"{self.icons.debug} ",
                "bullet_icon": f"{self.icons.bullet} ",
            }
        )

    def transform_text(self, text: str, transform: str) -> str:
        """Apply text transformation based on theme settings.

        Args:
            text: Text to transform
            transform: Transformation type - "upper", "lower", "title", or "none"

        Returns:
            Transformed text string
        """
        if transform == "upper":
            return text.upper()
        if transform == "lower":
            return text.lower()
        if transform == "title":
            return text.title()
        return text
