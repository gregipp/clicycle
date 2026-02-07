<!-- markdownlint-configure-file {"MD024": { "siblings_only": true, "allow_different_nesting": true }} -->

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.3.1] - 2026-02-07

### Fixed

- README images now use absolute URLs for PyPI rendering

## [3.3.0] - 2026-02-07

### Added

- **Panel component:** Bordered content boxes with optional title and subtitle.
  `cc.panel("Content", title="Title", subtitle="Footer")`
- **Key-value component:** Dashboard-style aligned label:value displays.
  `cc.key_value({"Host": "prod-01", "CPU": "23%"})` — accepts dict or list of
  tuples
- **Spacer component:** Explicit vertical whitespace that bypasses automatic
  spacing. `cc.spacer()` for 1 line, `cc.spacer(3)` for multiple
- **Divider component:** Subtle horizontal rule for visual separation.
  `cc.divider()` — uses `Layout.divider_style`
- **`Layout.title_align`:** Global title alignment for panels, tables, and
  key-value components (default: `"left"`)
- **`Layout.table_expand`:** Tables expand to fill available width by default
- **`Layout.panel_box`**, **`Layout.panel_border_style`**,
  **`Layout.panel_expand`:** Panel appearance configuration
- **`Layout.divider_style`:** Divider color configuration

### Changed

- Section component now uses `theme.typography.section_style` and
  `theme.layout.divider_style` for consistent theme integration
- Table `expand` defaults to `theme.layout.table_expand` (true by default)

## [3.2.3] - 2026-01-09

### Added

- **Spinner transient parameter:** Added `transient` parameter to `cc.spinner()`
  allowing per-spinner control over disappearing behavior, overriding theme's
  `disappearing_spinners` setting. Use `cc.spinner("msg", transient=True)` to
  make a spinner disappear when done regardless of theme configuration.

## [3.2.2] - 2026-01-09

### Fixed

- Fixed test files using old Text component signature after cc.text() changes

## [3.2.1] - 2026-01-09

### Fixed

- Fixed import sorting issues

## [3.2.0] - 2026-01-09

### Added

- **Text Component:** Added `cc.text()` for displaying plain text without an icon

## [3.1.6] - 2025-10-05

### Fixed

- Fixed test expectations for console width handling (tests now properly check
  Clicycle.width instead of console.width)
- Added comprehensive test coverage for special attribute access and dynamic
  function creation

## [3.1.5] - 2025-10-05

### Added

- **Type Annotations:** Added comprehensive type stubs for all dynamically
  created convenience functions (`info`, `warning`, `section`, `table`, etc.) to
  improve mypy compatibility and IDE support

### Fixed

- Resolved mypy type checking issues for dynamically created module attributes
  by using `TYPE_CHECKING` imports

## [3.1.4] - 2025-08-06

### Added

- **Table Component Enhancements:** Added `column_widths` and `wrap_text`
  support to Table component for better text formatting control

## [3.1.3] - 2025-08-06

### Added

- **Code Component:** Enabled word wrapping for code component to improve
  readability of long code snippets

### Fixed

- Cleaned up linting issues in module interface code
- Resolved linting issues that were preventing CI/CD pipeline from passing

## [3.1.2] - 2025-08-06

### Fixed

- Cleaned up trailing whitespace in module interface code
- Resolved linting issues that were preventing CI/CD pipeline from passing

## [3.1.1] - 2025-08-06

### Added

- **Native PyInstaller support** - Clicycle now automatically detects and works
  in frozen environments without requiring wrapper files
- Graceful fallback when `sys.modules` replacement fails in frozen environments
- Test coverage for module interface initialization

### Changed

- Updated PyInstaller documentation to reflect automatic compatibility

### Fixed

- Module interface initialization now works automatically in PyInstaller frozen
  executables

## [3.1.0] - 2025-08-06

### Added

- **Performance Optimizations:**

  - Console instance caching for improved performance
  - Render history limiting (default 100 components) to prevent memory growth
  - Smart rendering pipeline optimizations

- **Input Validation:**

  - Text components now validate string inputs (TypeError for non-strings)
  - Empty string validation (ValueError for empty messages)
  - Theme parameter validation (width >= 20, valid spinner types)
  - Clear error messages for better developer experience

- **API Documentation:**

  - Comprehensive docstrings for all major components
  - Usage examples in docstrings
  - Parameter descriptions and type hints
  - Return value documentation

- **New Features:**
  - Validation example demonstrating error handling
  - "Coming Soon" roadmap in README

### Fixed

- Pytest coverage warning "module was previously imported but not measured"
- Trailing whitespace in docstrings (W293 linting issues)

### Changed

- Coverage path in pytest configuration from `--cov=clicycle` to
  `--cov=src/clicycle`
- Validation example now uses `contextlib.suppress` for cleaner code

## [3.0.0] - 2025-08-06

### Removed

- BREAKING: Debug component removed; use Python's standard `logging` module
  instead
- BREAKING: Removed all `cc.debug()` functionality
- BREAKING: Removed Click context integration for verbose/debug mode

### Changed

- Debug messages now use Python's standard logging module
- `--verbose` flag replaced with `--debug` in examples
- No more inline imports throughout the codebase

### Added

- `py.typed` marker for better type checking support
- E402 linting rule to catch inline imports

### Fixed

- Removed all inline imports that could cause circular dependencies
- Fixed redundant icons in example files

### Migration Guide

Replace debug component usage:

```python
# Old (no longer works):
cc.debug("Debug message")

# New:
import logging
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

## [2.2.5] - 2025-08-06

### Fixed

- Debug components no longer affect spacing when not rendered (verbose mode off)
- Fixed spinner style persistence issue in full_app.py example

### Added

- Verbose mode example (full_app_verbose.py) to demonstrate debug messages
- Comprehensive debug documentation in README
- More debug messages throughout full_app.py for better demonstration

## [2.2.4] - 2025-08-06

### Fixed

- Fixed incorrect table usage in all_components.py example (was using
  non-existent headers/rows parameters)

## [2.2.3] - 2025-08-06

### Fixed

- Removed all references to the removed summary component from examples
- Replaced summary usage with simple info outputs

## [2.2.2] - 2025-08-06

### Fixed

- Fixed whitespace linting issues in test files

## [2.2.1] - 2025-08-06

### Fixed

- app_name now properly displays in headers when configured via
  `cc.configure(app_name="MyApp")` or `Clicycle(app_name="MyApp")`

## [2.2.0] - 2025-08-06

### Added

- `prompt()`, `confirm()`, and `select_list()` functions for user input
- Comprehensive integration tests for prompt components
- Stream orchestrator tests achieving 100% coverage

### Fixed

- Test architecture now properly tests clicycle wrappers instead of bypassing
  them
- Improved test coverage to 96% overall

### Changed

- Refactored prompt components to use render() method consistently
- Tests now validate the full clicycle flow rather than mocking internals

## [2.1.4] - 2025-08-06

### Fixed

- Removed debug print statements that were accidentally left in v2.1.3

## [2.1.3] - 2025-08-06

### Fixed

- Fixed blank line appearing between progress bar descriptions and actual
  progress bars
- Fixed spacing issues for persistent (non-disappearing) spinners
- Improved deferred rendering architecture for progress/spinner components
- Fixed debug components interfering with live displays
- Changed default `disappearing_spinners` to `False` for better UX

### Changed

- Introduced `deferred_render` flag for components that use context managers
- Improved stream orchestration to handle live context transitions properly
- Components now properly remain in history for spacing calculations

## [2.1.2] - 2025-01-06

### Fixed

- Actually includes the progress bar rendering fixes from v2.1.1 (v2.1.1 was
  released prematurely without the fixes)
- Progress bar description now correctly appears on its own line above the bar
- Fixed all test and linting issues

## [2.1.1] - 2025-01-06

### Fixed

- Progress bar description now appears on its own line above the bar for better
  readability
- Removed duplicate percentage display in progress bars
- Fixed spacing issues between progress/spinner components and other components
- Progress and spinner components no longer cause double rendering

## [2.1.0] - 2025-01-06

### Added

- `multi_progress()` context manager for tracking multiple concurrent tasks
- `group()` context manager for rendering components without spacing (formerly
  `block()`)
- New `modifiers` module for non-component rendering modifiers
- Dedicated example for demonstrating group functionality
  (`examples/features/groups.py`)
- Multi-task progress tracking in all_components example

### Fixed

- Progress bar context manager now properly handles updates
- Menu example no longer displays ANSI codes when arrow keys are pressed after
  "Press Enter to continue"
- All linting issues resolved (ruff and mypy clean)

### Changed

- Refactored menu.py to reduce complexity by extracting helper functions
- Improved code organization with separate `modifiers` directory

## [2.0.2] - 2025-01-05

### Fixed

- Updated PyPI version badge to use shields.io instead of badge.fury.io for
  better reliability
- Badge now correctly shows the latest PyPI version without caching delays

## [2.0.1] - 2025-01-05

### Fixed

- Added comprehensive type annotations for mypy strict mode compliance
- Fixed type compatibility issues in prompt and interactive components
- Updated all `__exit__` methods to use `Literal[False]` return type
- Fixed module import approach in interactive components to avoid attribute
  errors
- Ensured all components pass mypy strict mode checks

### Changed

- Updated test assertions to match new type annotation behavior

## [2.0.0] - 2025-01-05

### Added

- Component-based architecture with automatic spacing management
- Interactive components with arrow-key navigation (`select` and `multi_select`)
- Disappearing spinners feature with `disappearing_spinners` theme option
- Convenient module-level API (`import clicycle as cc`)
- Debug component that respects Click's verbose mode
- Comprehensive test suite with 96% coverage
- Full type hints throughout the codebase
- Python 3.11+ support

### Changed

- Complete architectural refactor from monolithic to component-based design
- Moved from class-based to function-based API for better ergonomics
- Components now self-manage spacing based on theme rules
- Spinners now properly handle transient display when disappearing
- Improved Rich integration with better theme customization
- Updated minimum Python version from 3.10 to 3.11

### Fixed

- Double messaging issue with spinners
- Spacing issues between components
- Interactive menu display issues across different terminals
- Test coverage gaps and import errors

### Removed

- Legacy monolithic `core.py` module
- Old class-based API (though Clicycle class still available for advanced use)
- Python 3.10 support

## [1.0.0] - 2024-12-12

### Added

- Initial release
- Basic CLI rendering with Rich styling
- Header, section, and text components
- Progress bars and spinners
- Table and summary components
- Theme system with customizable icons and colors
