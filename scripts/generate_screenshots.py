"""Generate SVG screenshots of clicycle components for documentation.

Uses Rich's Console(record=True) + console.save_svg() to capture
terminal output as sharp, scalable SVGs for GitHub READMEs.

Usage:
    uv run python scripts/generate_screenshots.py
"""

from __future__ import annotations

from pathlib import Path

from rich import box as rich_box
from rich.console import Console
from rich.panel import Panel as RichPanel
from rich.table import Table as RichTable
from rich.text import Text as RichText

OUTPUT_DIR = Path(__file__).parent.parent / "docs" / "images"
WIDTH = 80


def generate_quickstart() -> None:
    """Render the quick-start hello-world flow."""
    console = Console(width=WIDTH, record=True)

    # Header
    console.print(RichText("MY APP", style="bold white"))
    console.print(RichText("v2.0.0", style="dim white"))
    console.print()

    # Info
    console.print("ℹ Starting process...", style="cyan")
    console.print()

    # Spinner result (can't animate, show completed state)
    console.print("✔ Processing complete", style="bold green")
    console.print()

    # Table
    table = RichTable(
        box=rich_box.HEAVY_HEAD,
        border_style="bright_black",
        header_style="bold",
        expand=True,
        title_justify="left",
    )
    table.add_column("Name")
    table.add_column("Score")
    table.add_row("Alice", "95")
    table.add_row("Bob", "87")
    console.print(table)

    console.save_svg(str(OUTPUT_DIR / "quickstart.svg"), title="clicycle — Quick Start")


def generate_components() -> None:
    """Render a showcase of structural components."""
    console = Console(width=WIDTH, record=True)

    # Panel
    panel = RichPanel(
        "All systems operational.\nNo incidents reported in the last 24 hours.",
        title="Status",
        title_align="left",
        subtitle="Updated 2m ago",
        subtitle_align="right",
        box=rich_box.ROUNDED,
        border_style="bright_black",
        expand=True,
    )
    console.print(panel)
    console.print()

    # Key-value pairs (borderless table)
    kv_table = RichTable(
        title="Server Info",
        title_justify="left",
        box=None,
        show_header=False,
        padding=(0, 1),
        expand=False,
    )
    kv_table.add_column(style="bold")
    kv_table.add_column(style="default")
    kv_table.add_row("Host", "prod-01.us-east")
    kv_table.add_row("Uptime", "14d 3h 22m")
    kv_table.add_row("CPU", "23%")
    kv_table.add_row("Memory", "4.2 / 8.0 GB")
    console.print(kv_table)
    console.print()

    # Divider
    console.rule(style="bright_black")
    console.print()

    # Section
    console.rule(
        "[bold bright_blue]DEPLOYMENT[/]",
        style="bright_black",
        align="right",
    )
    console.print()

    # Messages
    console.print("ℹ Building containers...", style="cyan")
    console.print("ℹ Pushing to registry...", style="cyan")
    console.print("✔ Deployed to production", style="bold green")
    console.print("⚠ Rate limit at 80%", style="bold yellow")
    console.print()

    # Table
    table = RichTable(
        title="Services",
        title_justify="left",
        box=rich_box.HEAVY_HEAD,
        border_style="bright_black",
        header_style="bold",
        expand=True,
    )
    table.add_column("Service")
    table.add_column("Status")
    table.add_column("Latency")
    table.add_row("API Gateway", "✔ Healthy", "12ms")
    table.add_row("Auth Service", "✔ Healthy", "8ms")
    table.add_row("Database", "⚠ Degraded", "145ms")
    console.print(table)

    console.save_svg(str(OUTPUT_DIR / "components.svg"), title="clicycle — Components")


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    generate_quickstart()
    generate_components()
    print(f"SVGs saved to {OUTPUT_DIR}/")
    for svg in sorted(OUTPUT_DIR.glob("*.svg")):
        print(f"  {svg.name}")
