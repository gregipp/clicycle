"""Clicycle - Component-based CLI rendering with automatic spacing."""

from __future__ import annotations

import inspect
import sys
from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING, Any

from clicycle.clicycle import Clicycle
from clicycle.components.spinner import Spinner
from clicycle.theme import (
    ComponentIndentation,
    ComponentSpacing,
    Icons,
    Layout,
    Theme,
    Typography,
)

if TYPE_CHECKING:
    # Type annotations for dynamically created convenience functions
    def text(message: str) -> None: ...
    def info(message: str) -> None: ...
    def warning(message: str) -> None: ...
    def error(message: str) -> None: ...
    def success(message: str) -> None: ...
    def debug(message: str) -> None: ...
    def list_item(message: str) -> None: ...
    def section(title: str) -> None: ...
    def table(
        data: list[dict[str, Any]],
        title: str | None = None,
        **kwargs: Any,
    ) -> None: ...
    def header(
        title: str,
        subtitle: str | None = None,
        app_name: str | None = None,
    ) -> None: ...
    def code(
        content: str,
        language: str = "python",
        title: str | None = None,
        line_numbers: bool = True,
    ) -> None: ...
    def json(data: Any, title: str | None = None) -> None: ...
    def spinner(message: str = "Processing") -> Spinner: ...
    def progress(description: str = "Processing") -> Any: ...
    def multi_progress(description: str = "Processing") -> Any: ...
    def group() -> Any: ...
    def prompt(text: str, **kwargs: Any) -> Any: ...
    def confirm(text: str, **kwargs: Any) -> bool: ...
    def select(
        item_name: str, options: list[str], default: str | None = None
    ) -> str: ...
    def multi_select(
        item_name: str, options: list[str], default: list[str] | None = None
    ) -> list[str]: ...
    def select_list(
        item_name: str, options: list[str], default: str | None = None
    ) -> str: ...


__version__ = "3.2.0"

# Core exports
__all__ = [
    "Clicycle",
    "Theme",
    "Icons",
    "Typography",
    "Layout",
    "ComponentSpacing",
    "ComponentIndentation",
]


class _ModuleInterface(ModuleType):
    """Module wrapper that provides convenience API."""

    def __init__(self, module: ModuleType) -> None:
        self.__dict__.update(module.__dict__)
        self._cli = Clicycle()
        self._component_cache: dict[str, tuple[str, str]] = {}
        self._discover_components()

    def _discover_components(self) -> None:
        """Discover all components in the components directory."""
        components_dir = Path(__file__).parent / "components"

        for py_file in components_dir.glob("*.py"):
            if py_file.name.startswith("_") or py_file.name == "base.py":
                continue

            module_name = f"clicycle.components.{py_file.stem}"
            module = __import__(module_name, fromlist=["*"])

            # Find all classes that inherit from Component
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if hasattr(obj, "component_type") and obj.__module__ == module_name:
                    # Skip interactive components that need ask()
                    if hasattr(obj, "ask"):
                        continue
                    # Use component_type as the convenience name
                    self._component_cache[obj.component_type] = (module_name, name)

    def __getattr__(self, name: str) -> Any:
        """Get attribute from module, component cache, or special handlers."""
        # Dispatch to handlers
        for handler in [
            self._handle_special_attribute,
            self._handle_cached_component,
            self._handle_special_function,
        ]:
            # The sentinel is used to distinguish from a handler returning None
            sentinel = object()
            result = handler(name, sentinel)
            if result is not sentinel:
                return result

        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

    def _handle_special_attribute(self, name: str, sentinel: object) -> Any:
        """Handle special attributes like 'console', 'theme', etc."""
        if name == "console":
            return self._cli.console
        if name == "theme":
            return self._cli.theme
        if name == "configure":

            def configure(**kwargs: Any) -> None:
                self._cli = Clicycle(**kwargs)

            return configure
        if name == "clear":
            return self._cli.clear
        return sentinel

    def _handle_cached_component(self, name: str, sentinel: object) -> Any:
        """Handle components that are in the cache."""
        if name not in self._component_cache:
            return sentinel

        module_name, class_name = self._component_cache[name]
        module = __import__(module_name, fromlist=[class_name])
        component_class = getattr(module, class_name)

        # Create wrapper function based on component type
        if hasattr(component_class, "__enter__"):
            # Context managers need console
            def context_wrapper(message: str) -> Any:
                obj = component_class(self._cli.theme, message, self._cli.console)
                self._cli.stream.render(obj)
                return obj

            wrapper = context_wrapper
        else:
            # Regular components
            def regular_wrapper(*args: Any, **kwargs: Any) -> None:
                # For Header component, inject app_name if not provided
                if name == "header" and "app_name" not in kwargs and self._cli.app_name:
                    kwargs["app_name"] = self._cli.app_name

                obj = component_class(self._cli.theme, *args, **kwargs)
                self._cli.stream.render(obj)

            wrapper = regular_wrapper

        wrapper.__name__ = name
        wrapper.__doc__ = f"Display {name.replace('_', ' ')}."

        # Cache and return
        setattr(self, name, wrapper)
        return wrapper

    def _handle_special_function(self, name: str, sentinel: object) -> Any:
        """Handle special functions that are not auto-discovered."""
        # Try different handler groups
        handlers = [
            self._handle_json_function,
            self._handle_interactive_functions,
            self._handle_progress_function,
            self._handle_group_function,
            self._handle_prompt_functions,
        ]

        for handler in handlers:
            result = handler(name)
            if result is not None:
                setattr(self, name, result)
                return result

        return sentinel

    def _handle_json_function(self, name: str) -> Any:
        """Handle JSON function."""
        if name == "json":
            from clicycle.components.code import json_code

            def json_wrapper(data: Any, title: str | None = None) -> None:
                self._cli.stream.render(json_code(self._cli.theme, data, title))

            return json_wrapper
        return None

    def _handle_interactive_functions(self, name: str) -> Any:
        """Handle interactive select functions."""
        if name == "select":
            from clicycle.interactive.select import interactive_select

            return interactive_select

        if name == "multi_select":
            from clicycle.interactive.multi_select import interactive_multi_select

            return interactive_multi_select

        return None

    def _handle_progress_function(self, name: str) -> Any:
        """Handle multi_progress function."""
        if name == "multi_progress":
            from clicycle.components.multi_progress import MultiProgress

            def multi_progress_wrapper(description: str = "Processing") -> Any:
                obj = MultiProgress(self._cli.theme, description, self._cli.console)
                self._cli.stream.render(obj)
                return obj

            return multi_progress_wrapper
        return None

    def _handle_group_function(self, name: str) -> Any:
        """Handle group context manager."""
        if name == "group":

            def group_wrapper() -> Any:
                return self._cli.group()

            return group_wrapper
        return None

    def _handle_prompt_functions(self, name: str) -> Any:
        """Handle prompt component functions."""
        if name == "prompt":
            from clicycle.components.prompt import Prompt

            def prompt_wrapper(text: str, **kwargs: Any) -> Any:
                obj = Prompt(self._cli.theme, text, **kwargs)
                # Input components go through stream for spacing
                self._cli.stream.render(obj)
                return obj.ask()

            return prompt_wrapper

        if name == "confirm":
            from clicycle.components.prompt import Confirm

            def confirm_wrapper(text: str, **kwargs: Any) -> bool:
                obj = Confirm(self._cli.theme, text, **kwargs)
                # Input components go through stream for spacing
                self._cli.stream.render(obj)
                return obj.ask()

            return confirm_wrapper

        if name == "select_list":
            from clicycle.components.prompt import SelectList

            def select_list_wrapper(
                item_name: str,
                options: list[str],
                default: str | None = None,
            ) -> str:
                obj = SelectList(self._cli.theme, item_name, options, default)
                # Go through the stream for proper spacing
                self._cli.stream.render(obj)
                return obj.ask()

            return select_list_wrapper

        return None


# Replace this module with our wrapper
# Handle PyInstaller frozen environments
def _initialize_module_interface() -> bool:
    """Initialize the module interface, handling frozen environments."""
    try:
        # Try normal module replacement
        interface = _ModuleInterface(sys.modules[__name__])
        sys.modules[__name__] = interface
        return True
    except Exception:
        # In frozen environments, the replacement might fail
        # Set up the interface manually by adding methods to current module
        current_module = sys.modules[__name__]
        interface = _ModuleInterface(current_module)

        # Copy all interface methods to current module
        for attr_name in dir(interface):
            if not attr_name.startswith("_"):
                setattr(current_module, attr_name, getattr(interface, attr_name))

        return False


# Initialize the interface
_initialize_module_interface()
