#!/usr/bin/env python3
"""Demonstrate ``cc.indent(n)`` for visual hierarchy without per-component params.

Every component rendered inside the block is indented by ``n`` spaces. Tables,
messages, panels, key-value blocks — anything that prints through the
clicycle stream. Nesting composes: an outer ``indent(2)`` wrapping an inner
``indent(2)`` indents inner content by 4.
"""

import clicycle as cc

cc.header("Indent", "Nested layouts without per-component prefixes")

cc.section("Build pipeline")
cc.info("Top-level status:")

with cc.indent(2):
    cc.subsection("Compile")
    cc.info("Compiling sources...")
    cc.table(
        [
            {"File": "main.c", "Result": "ok"},
            {"File": "util.c", "Result": "ok"},
        ],
        show_header=False,
        box="simple",
    )

    cc.subsection("Link")
    with cc.indent(2):
        cc.info("Resolving symbols...")
        cc.success("Built target binary")

cc.info("Back at the top level.")
