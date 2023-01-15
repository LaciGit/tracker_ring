from datetime import datetime
import param
import panel as pn

from tracker.db import Controller

pn.extension()
pn.extension(sizing_mode="stretch_width")

if "controller" in pn.state.cache:
    controller = pn.state.cache["controller"]
else:
    pn.state.cache["controller"] = controller = Controller()

ACCENT_COLOR = pn.template.ReactTemplate.header_color


class PlotView(param.Parameterized):

    year_week = param.Boolean(True, doc="Display data in 'YearWeek'")

    def __init__(self, **params):
        super().__init__(**params)

        widgets = {
            "year_week": {
                "type": pn.widgets.Checkbox,
                "disabled": False,
            }
        }
        self.controls = pn.Param(self, widgets=widgets)


PLOT_VIEW = PlotView()
