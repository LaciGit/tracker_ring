import panel as pn

from tracker import SETTINGS, __version__
from tracker.dashboard import (
    SIDEBAR,
    DURATION_PLTOS,
    SUNBURST,
    KPI_TAGS,
    CONTROLLER,
)

from tracker.db import Controller

pn.extension(
    sizing_mode="stretch_both",
    notifications=True,
)

if "controller" in pn.state.cache:
    controller = pn.state.cache["controller"]
else:
    pn.state.cache["controller"] = controller = Controller()


template = pn.template.ReactTemplate(title=f"{SETTINGS.app_name} v{__version__}")

template.sidebar.append(SIDEBAR)

template.main[:3, :8] = DURATION_PLTOS.create_plot_1
template.main[:3, 8:] = SUNBURST.create_plot
template.main[3:5, :8] = DURATION_PLTOS.create_plot_2
template.main[3:5, 8:] = KPI_TAGS.create_plot
template.main[5:, :] = CONTROLLER

template.sidebar_width = 350
template.header_background = "#428bca"

template.servable()
