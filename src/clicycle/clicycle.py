"""Main Clicycle class - simple orchestrator for CLI components."""

from __future__ import annotations

import io
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from rich.console import Console
from rich.text import Text

from clicycle.rendering.stream import RenderStream
from clicycle.theme import Theme


class Clicycle:
    """Main orchestrator for component-based CLI rendering.

    The central class that manages console output, theming, and component rendering.
    Provides automatic spacing between components based on theme rules.
    Caches console instances for performance optimization.

    Args:
        width: Console width in characters (default: 100)
        theme: Theme configuration for styling and spacing (default: Theme())
        app_name: Optional application name for branding in headers

    Attributes:
        width: Console width setting
        theme: Active theme configuration
        console: Rich console instance (cached by width)
        stream: RenderStream for managing component history and spacing
        app_name: Application name for branding

    Example:
        >>> from clicycle import Clicycle
        >>> cli = Clicycle(width=120, app_name="MyApp")
        >>> # Components will use this instance's theme and console
    """

    _console_cache: dict[int, Console] = {}

    def __init__(
        self, width: int = 100, theme: Theme | None = None, app_name: str | None = None
    ):
        self.width = width
        self.theme = theme or Theme()
        # Reuse console instances for the same width
        if width not in Clicycle._console_cache:
            Clicycle._console_cache[width] = Console(width=width)
        self.console = Clicycle._console_cache[width]
        self.stream = RenderStream(self.console)
        self.app_name = app_name

    def clear(self) -> None:
        """Clear the console screen and reset component history.

        Useful for starting fresh displays or implementing screen updates.
        """
        self.console.clear()
        self.stream.clear_history()

    @contextmanager
    def indent(self, spaces: int) -> Iterator[Clicycle]:
        """Indent every component rendered inside the block by ``spaces``.

        Each component renders normally (spacing rules, styles, colors), and
        on exit the buffered output is re-emitted to the real console with a
        leading-space prefix on every line. Nesting works: an outer
        ``indent(2)`` wrapping an inner ``indent(2)`` indents inner content by
        4 in total because both buffers replay through the parent.

        Args:
            spaces: Indent width. ``0`` or negative is a no-op.

        Yields:
            Self for use within the context.

        Example:
            >>> import clicycle as cc
            >>> cc.section("Build")
            >>> with cc.indent(2):
            ...     cc.info("Compiling")
            ...     cc.info("Linking")
        """
        if spaces <= 0:
            yield self
            return

        original_stream = self.stream
        original_console = self.console

        buffer = io.StringIO()
        # ``force_terminal=True`` is what gets us styled output (truecolor
        # ANSI in the buffer) even though the file is a StringIO. We don't
        # forward ``original_console.color_system`` — Rich's auto-detect under
        # force_terminal lands on the right setting and the stub's
        # ``str | None`` typing of ``Console.color_system`` doesn't match the
        # ``Literal[...] | None`` the constructor expects.
        buffer_console = Console(
            file=buffer,
            width=max(1, self.width - spaces),
            force_terminal=True,
            record=True,
        )
        self.console = buffer_console
        self.stream = RenderStream(buffer_console)

        try:
            yield self
        finally:
            self.console = original_console
            self.stream = original_stream

            captured = buffer_console.export_text(styles=True, clear=True)
            prefix = " " * spaces
            for line in captured.splitlines():
                # ``Text.from_ansi`` parses ANSI escape codes back into a
                # styled ``Text`` object, then ``console.print`` re-emits it
                # via ``_write_buffer``. That path matters: it's what feeds
                # an outer ``record=True`` console, so nested ``indent``
                # blocks compose correctly. A direct ``file.write`` would
                # bypass the recorder and lose inner content.
                original_console.print(
                    Text.from_ansi(f"{prefix}{line}") if line else Text(prefix)
                )

    @contextmanager
    def group(self) -> Iterator[Clicycle]:
        """Context manager for rendering components without spacing between them.

        Components rendered within this context will have no spacing between them,
        useful for creating compact layouts or related content groups.

        Yields:
            Self for use within the context

        Example:
            >>> import clicycle as cc
            >>> with cc.group():
            ...     cc.info("Line 1")  # No spacing between these
            ...     cc.info("Line 2")
            ...     cc.info("Line 3")
        """
        from clicycle.modifiers.group import Group

        # Store the current stream and console
        original_stream = self.stream
        original_console = self.console

        with Path("/dev/null").open("w") as dev_null_file:
            # Create temporary console and stream that won't actually display anything
            temp_console = Console(width=self.width, file=dev_null_file)
            temp_stream = RenderStream(temp_console)

            # Temporarily replace both the stream and console
            self.stream = temp_stream
            self.console = temp_console

            try:
                yield self
            finally:
                # Get all the components that were rendered to the temp stream
                components = temp_stream.history

                # Restore original stream and console
                self.stream = original_stream
                self.console = original_console

                # Render as group
                if components:
                    self.stream.render(Group(self.theme, components))
