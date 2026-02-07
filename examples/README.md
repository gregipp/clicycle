# Clicycle Examples

This directory contains example scripts demonstrating various features and use cases of the Clicycle CLI framework.

## Running the Examples

Make sure you have Clicycle installed (see [README](../README.md))

Run the interactive example menu:

```bash
python examples/menu.py
```

Or run any example directly:

```bash
python examples/basics/hello_world.py
python examples/features/themes.py
python examples/advanced/full_app.py
```

## Available Examples

### Basics

- **`basics/hello_world.py`** — Simple introduction to headers, messages, and tables
- **`basics/all_components.py`** — Tour of all components

### Features

- **`features/interactive.py`** — Arrow-key selection and multi-select menus
- **`features/spinners.py`** — Disappearing spinner functionality
- **`features/themes.py`** — Custom themes (emoji, minimal, matrix)
- **`features/groups.py`** — Grouping components without spacing
- **`features/prompts.py`** — User input prompts and confirmations
- **`features/validation.py`** — Input validation and error handling

### Advanced

- **`advanced/full_app.py`** — Complete application showcase
- **`advanced/full_app_debug.py`** — Full app with debug logging enabled

## What to Look For

When running the examples, pay attention to:

- **Automatic spacing** between components
- **Consistent styling** across different message types
- **Smart table formatting** that adapts to content
- **Progress feedback** during long operations
- **Theme customization** possibilities
