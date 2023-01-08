import panel as pn

from tracker.dashboard.params.controller import AREA
from tracker.dashboard import DATA_HANDLER
from tracker.db import Controller

pn.extension()

if "controller" in pn.state.cache:
    controller = pn.state.cache["controller"]
else:
    pn.state.cache["controller"] = controller = Controller()


tabs = pn.Tabs(
    (
        "Area",
        pn.Row(AREA.controls, controller.get_unique(cls="area")),
    ),
    ("Topic", ""),
    ("Task", ""),
    ("Tag", ""),
    # active=2,
    dynamic=True,
)

CONTROLLER = pn.Card(
    tabs,
    title="Controller",
    # collapsed=True,
    collapsible=True,
)
