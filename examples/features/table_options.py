#!/usr/bin/env python3
"""Demonstrate the per-call ``show_header`` and ``box`` options on ``cc.table``.

Both let one call deviate from the theme without configuring a new theme:

- ``show_header=False`` drops the column-name header row entirely. Useful when
  the columns are obvious from the values (status icon + name + tag) and the
  extra row is noise.
- ``box=`` picks a Rich box style for this call only. Friendly names like
  ``"simple"`` or ``"minimal"`` resolve via ``clicycle.box()``; you can also
  pass a ``rich.box.Box`` directly.
- ``no_wrap=`` names the columns that never wrap, so a narrow console folds
  the prose column and leaves identifiers on one line.
- ``show_edge=False`` drops the box's top and bottom edges for an aligned
  block with no frame.
"""

import clicycle as cc

cc.header("Table Options", "show_header, box, no_wrap and show_edge per call")

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

STATUS_ROWS = [
    {"Service": "hub", "Release": "8e94fce", "State": "✔ Synced · Healthy"},
    {
        "Service": "auth",
        "Release": "8e94fce → 69e358f",
        "State": "⚠ no deploy running, 2 commits behind",
    },
]

cc.section("no_wrap=(...)")
cc.info("Rendered at 50 columns: the identifiers hold, the state folds.")
cc.configure(width=50)
cc.table(STATUS_ROWS, no_wrap=("Service", "Release"))

cc.section("show_edge=False")
cc.info("With box='simple' and no header: an aligned block with no frame.")
cc.table(
    STATUS_ROWS,
    no_wrap=("Service", "Release"),
    show_header=False,
    show_edge=False,
    box="simple",
)
