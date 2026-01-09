#!/usr/bin/env python3
"""Example showing all available components in clicycle."""

import time

import clicycle as cc

# Header with full information
cc.header("Clicycle Components", "Complete Reference", "Demo App")

# Text components
cc.section("Text Components")
cc.info("This is an info message - general information")
cc.success("This is a success message - operation completed")
cc.error("This is an error message - something went wrong")
cc.warning("This is a warning message - be careful")
cc.text("This is plain text - no icon, just styled text")
cc.text("Use text for paragraphs or labels that don't need a status icon. This command will sync your local configuration with the remote server. Any changes made locally will be uploaded, and any remote changes will be pulled down.")

# List items
cc.info("Here's a list of features:")
cc.list_item("Automatic spacing between components")
cc.list_item("Rich formatting and colors")
cc.list_item("Disappearing spinners")
cc.list_item("Progress bars with descriptions")

# Data display
cc.section("Data Display")

# Tables
users = [
    {"Name": "Alice Johnson", "Department": "Engineering", "Years": 5},
    {"Name": "Bob Smith", "Department": "Marketing", "Years": 3},
    {"Name": "Charlie Brown", "Department": "Sales", "Years": 7},
]
cc.table(users, title="Employee Directory")

# Code display
cc.code(
    """def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)""",
    language="python",
    title="Fibonacci Function",
)

# JSON display
config = {
    "app": {
        "name": "Clicycle Demo",
        "version": "2.0.0",
        "features": ["components", "themes", "spinners"],
    }
}
cc.json(config, title="Application Config")

# Table data
cc.table(
    [
        {"Metric": "Total Users", "Value": "1250"},
        {"Metric": "Active Sessions", "Value": "342"},
        {"Metric": "CPU Usage", "Value": "45%"},
        {"Metric": "Memory", "Value": "2.1 GB"},
    ],
    title="System Metrics",
)

# Progress indicators
cc.section("Progress Indicators")

# Spinner
cc.info("Regular spinner (message remains):")
with cc.spinner("Processing data..."):
    time.sleep(2)
cc.success("Processing complete!")

# Progress bar
cc.info("Progress bar with updates:")
with cc.progress("Downloading files") as prog:
    for i in range(101):
        prog.update(i, f"file_{i}.dat")
        time.sleep(0.02)
cc.success("Download complete!")

# Multi-task progress
cc.info("Multi-task progress (concurrent tasks):")
with cc.multi_progress("Processing multiple tasks") as progress:
    task1 = progress.add_task("[cyan]Download", total=100, short_id="DL")
    task2 = progress.add_task("[green]Process", total=80, short_id="PR")
    task3 = progress.add_task("[yellow]Upload", total=60, short_id="UP")

    for i in range(100):
        progress.update(task1, advance=1)
        if i >= 20:
            progress.update(task2, advance=1)
        if i >= 40:
            progress.update(task3, advance=1)
        time.sleep(0.02)
cc.success("All tasks complete!")

# Spacing demonstration
cc.section("Automatic Spacing")
cc.info("Components manage their own spacing.")
cc.info("Notice: no space between consecutive info messages.")
cc.info("This creates a clean, grouped appearance.")
cc.success("But different component types have appropriate spacing.")
cc.error("This error has space before it.")

# Group demonstration - components without spacing
cc.section("Grouped Content")
cc.info("Using group() to combine components without spacing:")
with cc.group():
    cc.info("These components")
    cc.success("are grouped together")
    cc.warning("without the usual")
    cc.error("spacing between them")
cc.info("This is outside the group and has normal spacing.")

# Clear example (commented out to not clear the demo)
# cc.clear()  # Would clear the screen

cc.section("Demo Complete")
cc.success("All components demonstrated!")
