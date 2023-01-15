import panel as pn

from tracker.dashboard.params.controller import AREA, TOPIC, TASK, TAG
from tracker.dashboard import DATA_HANDLER
from tracker.db import Controller

pn.extension(
    sizing_mode="stretch_width",
    notifications=True,
)

if "controller" in pn.state.cache:
    controller = pn.state.cache["controller"]
else:
    pn.state.cache["controller"] = controller = Controller()


tabs = pn.Tabs(
    (
        "Area",
        pn.Row(AREA.controls),
    ),
    (
        "Topic",
        pn.Row(TOPIC.controls),
    ),
    (
        "Task",
        pn.Row(TASK.controls),
    ),
    (
        "Tag",
        pn.Row(TAG.controls),
    ),
    active=2,
    dynamic=True,
)

CONTROLLER = pn.Card(
    tabs,
    title="Controller",
    collapsed=True,
    collapsible=True,
)
