"""Tests for the Theme system."""

from rich import box as rich_box

from clicycle import Theme
from clicycle.theme import ComponentSpacing, Icons, Layout, Typography


class TestIcons:
    """Test the Icons class."""

    def test_default_icons(self):
        """Test default icon values."""
        icons = Icons()

        assert icons.success == "✔"
        assert icons.error == "✖"
        assert icons.warning == "⚠"
        assert icons.info == "ℹ"
        assert icons.bullet == "•"

    def test_custom_icons(self):
        """Test custom icon values."""
        icons = Icons(success="✅", error="❌", info="💡")

        assert icons.success == "✅"
        assert icons.error == "❌"
        assert icons.info == "💡"
        # Defaults should still work
        assert icons.warning == "⚠"


class TestTypography:
    """Test the Typography class."""

    def test_default_typography(self):
        """Test default typography values."""
        typography = Typography()

        assert typography.header_style == "bold white"
        assert typography.success_style == "bold green"
        assert typography.error_style == "bold red"
        assert typography.header_transform == "upper"

    def test_custom_typography(self):
        """Test custom typography values."""
        typography = Typography(
            header_style="bold magenta", success_style="green", header_transform="title"
        )

        assert typography.header_style == "bold magenta"
        assert typography.success_style == "green"
        assert typography.header_transform == "title"
        # Defaults should still work
        assert typography.error_style == "bold red"


class TestLayout:
    """Test the Layout class."""

    def test_default_layout(self):
        """Test default layout values."""
        layout = Layout()

        assert layout.title_align == "left"
        assert layout.table_box == rich_box.HEAVY_HEAD
        assert layout.table_border_style == "bright_black"
        assert layout.table_expand is True
        assert layout.panel_box == rich_box.ROUNDED
        assert layout.panel_border_style == "bright_black"
        assert layout.panel_expand is True
        assert layout.divider_style == "bright_black"
        assert layout.url_style == "full"

    def test_custom_layout(self):
        """Test custom layout values."""
        layout = Layout(
            title_align="center",
            table_box=rich_box.ROUNDED,
            table_border_style="blue",
            table_expand=False,
            panel_box=rich_box.DOUBLE,
            panel_border_style="cyan",
            panel_expand=False,
            divider_style="dim white",
        )

        assert layout.title_align == "center"
        assert layout.table_box == rich_box.ROUNDED
        assert layout.table_border_style == "blue"
        assert layout.table_expand is False
        assert layout.panel_box == rich_box.DOUBLE
        assert layout.panel_border_style == "cyan"
        assert layout.panel_expand is False
        assert layout.divider_style == "dim white"
        assert layout.url_style == "full"


class TestComponentSpacing:
    """Test the ComponentSpacing class."""

    def test_default_spacing(self):
        """Test default spacing values."""
        spacing = ComponentSpacing()

        assert spacing.info == {"info": 0}
        assert spacing.debug == {"debug": 0}
        assert "info" in spacing.code
        assert "code" in spacing.code

    def test_custom_spacing(self):
        """Test custom spacing values."""
        spacing = ComponentSpacing(info={"info": 1}, code={"info": 2, "code": 1})

        assert spacing.info == {"info": 1}
        assert spacing.code == {"info": 2, "code": 1}


class TestTheme:
    """Test the complete Theme class."""

    def test_default_theme(self):
        """Test theme with all defaults."""
        theme = Theme()

        assert isinstance(theme.icons, Icons)
        assert isinstance(theme.typography, Typography)
        assert isinstance(theme.layout, Layout)
        assert isinstance(theme.spacing, ComponentSpacing)
        assert theme.width == 100
        assert theme.indent == "  "

    def test_custom_theme(self):
        """Test theme with custom components."""
        custom_icons = Icons(success="✅")
        custom_typography = Typography(header_style="bold magenta")
        custom_layout = Layout(table_box=rich_box.ROUNDED)
        custom_spacing = ComponentSpacing(info={"info": 1})

        theme = Theme(
            icons=custom_icons,
            typography=custom_typography,
            layout=custom_layout,
            spacing=custom_spacing,
            width=120,
            indent="    ",
        )

        assert theme.icons is custom_icons
        assert theme.typography is custom_typography
        assert theme.layout is custom_layout
        assert theme.spacing is custom_spacing
        assert theme.width == 120
        assert theme.indent == "    "

    def test_text_transform_upper(self):
        """Test text transformation - upper case."""
        theme = Theme()
        result = theme.transform_text("hello world", "upper")
        assert result == "HELLO WORLD"

    def test_text_transform_lower(self):
        """Test text transformation - lower case."""
        theme = Theme()
        result = theme.transform_text("HELLO WORLD", "lower")
        assert result == "hello world"

    def test_text_transform_title(self):
        """Test text transformation - title case."""
        theme = Theme()
        result = theme.transform_text("hello world", "title")
        assert result == "Hello World"

    def test_text_transform_none(self):
        """Test text transformation - no change."""
        theme = Theme()
        result = theme.transform_text("Hello World", "none")
        assert result == "Hello World"

    def test_text_transform_invalid(self):
        """Test text transformation - invalid transform type."""
        theme = Theme()
        result = theme.transform_text("Hello World", "invalid")
        assert result == "Hello World"  # Should return unchanged
