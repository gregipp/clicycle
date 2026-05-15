#!/usr/bin/env python3
"""Demonstrate ``cc.section`` and ``cc.subsection`` together.

``cc.section`` draws a full-width horizontal rule with the title floated
right — appropriate for top-level groupings of unrelated phases. When you
need a quieter break inside a section (a step within a phase, a child
grouping), ``cc.subsection`` prints just a styled title with no rule.
"""

import clicycle as cc

cc.header("Section + Subsection", "Two levels of header weight")

cc.section("Build")
cc.subsection("Compile")
cc.info("Compiling sources...")
cc.success("Compiled 12 modules")

cc.subsection("Link")
cc.info("Linking objects...")
cc.success("Built target binary")

cc.section("Deploy")
cc.subsection("Stage")
cc.info("Pushing to staging cluster")
cc.success("Stage deploy complete")

cc.subsection("Production")
cc.info("Awaiting approval...")
