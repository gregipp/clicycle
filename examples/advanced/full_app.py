#!/usr/bin/env python3
"""Complete showcase of all Clicycle components and features."""

import logging
import sys
import time

from clicycle import Clicycle
from clicycle.components.code import Code, json_code
from clicycle.components.divider import Divider
from clicycle.components.header import Header
from clicycle.components.key_value import KeyValue
from clicycle.components.panel import Panel
from clicycle.components.progress import ProgressBar
from clicycle.components.section import Section
from clicycle.components.spacer import Spacer
from clicycle.components.spinner import Spinner
from clicycle.components.table import Table
from clicycle.components.text import Error, Info, ListItem, Success, WarningText

logger = logging.getLogger(__name__)


def showcase_text_components(cli):
    """Demonstrate all text component types."""
    cli.stream.render(Section(cli.theme, "Text Components"))
    logger.debug("Starting text components demonstration")

    cli.stream.render(Info(cli.theme, "This is an info message"))
    logger.debug("Info messages use cyan color")

    cli.stream.render(Success(cli.theme, "This is a success message"))
    logger.debug("Success messages use green with checkmark icon")

    cli.stream.render(WarningText(cli.theme, "This is a warning message"))
    logger.debug("Warning messages use yellow with warning icon")

    cli.stream.render(Error(cli.theme, "This is an error message"))
    logger.debug("Error messages use red with X icon")

    logger.debug("Debug messages now use Python's standard logging")

    # List items
    cli.stream.render(Info(cli.theme, "Here's a list:"))
    logger.debug("List items are indented by 2 spaces by default")
    cli.stream.render(ListItem(cli.theme, "First item"))
    cli.stream.render(ListItem(cli.theme, "Second item"))
    cli.stream.render(ListItem(cli.theme, "Third item with a longer description"))
    logger.debug("List items have no spacing between them")


def showcase_headers_sections(cli):
    """Demonstrate headers and sections."""
    cli.stream.render(
        Header(
            cli.theme,
            "Main Application Title",
            "Version 2.0.0 - Complete Feature Showcase",
            "Clicycle Demo",
        )
    )

    cli.stream.render(Section(cli.theme, "Getting Started"))
    cli.stream.render(Info(cli.theme, "This section demonstrates headers and dividers"))

    cli.stream.render(Section(cli.theme, "Advanced Features"))
    cli.stream.render(
        Info(cli.theme, "Notice the automatic spacing between components")
    )


def showcase_tables(cli):
    """Demonstrate table rendering."""
    cli.stream.render(Section(cli.theme, "Tables"))

    # Simple table
    user_data = [
        {
            "Name": "Alice Johnson",
            "Age": 28,
            "Department": "Engineering",
            "Status": "Active",
        },
        {"Name": "Bob Smith", "Age": 34, "Department": "Marketing", "Status": "Active"},
        {
            "Name": "Charlie Brown",
            "Age": 22,
            "Department": "Sales",
            "Status": "Inactive",
        },
        {
            "Name": "Diana Prince",
            "Age": 31,
            "Department": "Engineering",
            "Status": "Active",
        },
    ]

    cli.stream.render(Table(cli.theme, user_data, title="Employee Directory"))

    # Table with mixed data types
    stats_data = [
        {"Metric": "Total Users", "Value": 1250, "Change": "+12.5%", "Status": "✅"},
        {"Metric": "Active Sessions", "Value": 342, "Change": "+5.2%", "Status": "✅"},
        {"Metric": "Error Rate", "Value": "0.02%", "Change": "-0.5%", "Status": "✅"},
        {"Metric": "Response Time", "Value": "142ms", "Change": "+8ms", "Status": "⚠️"},
    ]

    cli.stream.render(Table(cli.theme, stats_data, title="System Metrics"))


def showcase_code_components(cli):
    """Demonstrate code and JSON rendering."""
    cli.stream.render(Section(cli.theme, "Code Display"))

    # Python code
    python_code = '''def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Example usage
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")'''

    cli.stream.render(
        Code(
            cli.theme, python_code, language="python", title="Fibonacci Implementation"
        )
    )

    # JSON data
    config_data = {
        "app": {
            "name": "Clicycle Demo",
            "version": "2.0.0",
            "features": ["components", "themes", "spinners", "tables"],
            "settings": {"debug": False, "timeout": 30, "retries": 3},
        }
    }

    cli.stream.render(json_code(cli.theme, config_data, title="Configuration"))


def showcase_spinners(cli):
    """Demonstrate spinner functionality."""
    cli.stream.render(Section(cli.theme, "Spinners"))

    # Regular spinner
    cli.stream.render(
        Info(cli.theme, "Regular spinner (message remains after completion):")
    )
    spinner = Spinner(cli.theme, "Processing data...", cli.console)
    cli.stream.render(spinner)
    with spinner:
        time.sleep(2)

    cli.stream.render(Success(cli.theme, "Processing complete!"))

    # Different spinner styles
    spinner_styles = ["dots", "line", "star", "bouncingBar"]
    cli.stream.render(Info(cli.theme, "Different spinner styles:"))

    # Save original spinner type
    original_spinner = cli.theme.spinner_type

    for style in spinner_styles:
        cli.theme.spinner_type = style
        spinner = Spinner(cli.theme, f"Testing {style} spinner...", cli.console)
        cli.stream.render(spinner)
        with spinner:
            time.sleep(1.5)

    # Restore original spinner type
    cli.theme.spinner_type = original_spinner


def showcase_disappearing_spinners(cli):
    """Demonstrate disappearing spinners."""
    cli.stream.render(Section(cli.theme, "Disappearing Spinners"))

    # Save original setting
    original_disappearing = cli.theme.disappearing_spinners

    # Enable disappearing spinners for this demo
    cli.theme.disappearing_spinners = True

    cli.stream.render(
        Info(cli.theme, "Disappearing spinner (message vanishes after completion):")
    )

    spinner = Spinner(cli.theme, "This message will disappear...", cli.console)
    cli.stream.render(spinner)
    with spinner:
        time.sleep(2)

    cli.stream.render(Success(cli.theme, "Notice the spinner message is gone!"))

    # Nested spinners
    cli.stream.render(Info(cli.theme, "Nested disappearing spinners:"))

    spinner1 = Spinner(cli.theme, "Outer operation...", cli.console)
    cli.stream.render(spinner1)
    with spinner1:
        time.sleep(1)
        cli.stream.render(Info(cli.theme, "Starting inner task"))

        spinner2 = Spinner(cli.theme, "Inner operation...", cli.console)
        cli.stream.render(spinner2)
        with spinner2:
            time.sleep(1)

        cli.stream.render(Info(cli.theme, "Inner task complete"))
        time.sleep(1)

    cli.stream.render(Success(cli.theme, "All operations complete!"))

    # Restore original setting
    cli.theme.disappearing_spinners = original_disappearing


def showcase_progress_bars(cli):
    """Demonstrate progress bar functionality."""
    cli.stream.render(Section(cli.theme, "Progress Bars"))

    # Simple progress bar
    progress = ProgressBar(cli.theme, "Downloading files", cli.console)
    cli.stream.render(progress)

    with progress.track() as prog:
        for i in range(101):
            prog.update(i, f"Processing file_{i}.dat")
            time.sleep(0.02)

    cli.stream.render(Success(cli.theme, "Download complete!"))

    # Multiple progress bars
    cli.stream.render(Info(cli.theme, "Processing multiple tasks:"))

    tasks = ["Parsing", "Analyzing", "Optimizing"]
    for task in tasks:
        progress = ProgressBar(cli.theme, task, cli.console)
        cli.stream.render(progress)

        with progress.track() as prog:
            for i in range(101):
                prog.update(i)
                time.sleep(0.01)

        cli.stream.render(Success(cli.theme, f"{task} complete"))


def showcase_structural_components(cli):
    """Demonstrate panels, key-value pairs, dividers, and spacers."""
    cli.stream.render(Section(cli.theme, "Structural Components"))

    cli.stream.render(
        Panel(cli.theme, "All systems operational.", title="Status")
    )

    cli.stream.render(Spacer(cli.theme))

    cli.stream.render(
        Panel(
            cli.theme,
            "Rate limit approaching threshold.",
            title="Warning",
            subtitle="Updated 2m ago",
        )
    )

    cli.stream.render(Divider(cli.theme))

    cli.stream.render(
        KeyValue(
            cli.theme,
            {
                "Total Files": "1250",
                "Processed": "1248",
                "Failed": "2",
                "Success Rate": "99.84%",
            },
            title="Processing Stats",
        )
    )

    cli.stream.render(Spacer(cli.theme, lines=2))

    cli.stream.render(
        KeyValue(
            cli.theme,
            [
                ("Processing Time", "2m 34s"),
                ("Average Speed", "8.1 files/sec"),
            ],
            title="Performance",
        )
    )


def showcase_spacing_behavior(cli):
    """Demonstrate automatic spacing behavior."""
    cli.stream.render(Section(cli.theme, "Automatic Spacing"))

    cli.stream.render(Info(cli.theme, "Components automatically manage their spacing."))
    cli.stream.render(
        Info(cli.theme, "Notice: no space between consecutive info messages.")
    )
    cli.stream.render(Info(cli.theme, "This creates a clean, grouped appearance."))

    cli.stream.render(
        Success(cli.theme, "But different component types have appropriate spacing.")
    )

    cli.stream.render(Error(cli.theme, "This error has space before it."))

    cli.stream.render(Section(cli.theme, "New Section"))

    cli.stream.render(
        Info(cli.theme, "Sections always have proper spacing from previous content.")
    )


def main():
    """Run the complete showcase."""
    # Check for debug flag and configure logging
    debug = "--debug" in sys.argv or "-d" in sys.argv

    if debug:
        logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
    else:
        logging.basicConfig(level=logging.INFO)

    # Create CLI instance
    cli = Clicycle(app_name="Clicycle Showcase")

    if debug:
        cli.stream.render(
            Info(cli.theme, "Running in DEBUG mode - debug messages will be shown")
        )
    else:
        cli.stream.render(
            Info(
                cli.theme,
                "Running in NORMAL mode - debug messages hidden (use --debug to see them)",
            )
        )

    logger.debug("Application initialized")

    # Run all showcases
    showcase_headers_sections(cli)
    time.sleep(1)

    showcase_text_components(cli)
    time.sleep(1)

    showcase_tables(cli)
    time.sleep(1)

    showcase_code_components(cli)
    time.sleep(1)

    showcase_spinners(cli)
    time.sleep(1)

    showcase_disappearing_spinners(cli)
    time.sleep(1)

    showcase_progress_bars(cli)
    time.sleep(1)

    showcase_structural_components(cli)
    time.sleep(1)

    showcase_spacing_behavior(cli)

    # Final message
    cli.stream.render(Section(cli.theme, "Showcase Complete"))
    cli.stream.render(Success(cli.theme, "All components demonstrated successfully!"))
    cli.stream.render(
        Info(cli.theme, "Explore the examples directory for more specific use cases.")
    )


if __name__ == "__main__":
    main()
