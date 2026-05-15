#!/usr/bin/env python3
"""Demonstrate the per-call ``show_header`` and ``box`` options on ``cc.table``.

Both let one call deviate from the theme without configuring a new theme:

- ``show_header=False`` drops the column-name header row entirely. Useful when
  the columns are obvious from the values (status icon + name + tag) and the
  extra row is noise.
- ``box=`` picks a Rich box style for this call only. Friendly names like
  ``"simple"`` or ``"minimal"`` resolve via ``clicycle.box()``; you can also
  pass a ``rich.box.Box`` directly.
"""

import clicycle as cc

cc.header("Table Options", "show_header and box per call")

cc.section("Default")
cc.info("With the project theme — header row + theme box style.")
cc.table(
    [
        {"Service": "hub", "Tag": "8e94fce", "Status": "healthy"},
        {"Service": "auth", "Tag": "69e358f", "Status": "failing"},
    ]
)

cc.section("show_header=False")
cc.info("Drop the column-name row when context already makes them obvious.")
cc.table(
    [
        {"Service": "hub", "Tag": "8e94fce", "Status": "healthy"},
        {"Service": "auth", "Tag": "69e358f", "Status": "failing"},
    ],
    show_header=False,
)

cc.section("box='simple'")
cc.info("Lighter borders for inline tables that don't need to dominate.")
cc.table(
    [
        {"Service": "hub", "Tag": "8e94fce"},
        {"Service": "auth", "Tag": "69e358f"},
    ],
    show_header=False,
    box="simple",
)

cc.section("box='minimal'")
cc.info("Pass any BoxName (``rounded``, ``minimal``, ``heavy``, ...).")
cc.table(
    [
        {"Service": "hub", "Tag": "8e94fce"},
        {"Service": "auth", "Tag": "69e358f"},
    ],
    box="minimal",
)
