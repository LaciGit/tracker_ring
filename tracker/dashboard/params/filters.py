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


@pn.cache
def _get_unique():
    return dict(
        areas=controller.get_unique("area"),
        topics=controller.get_unique("topic"),
        tasks=controller.get_unique("task"),
        tags=controller.get_unique("tag"),
        times=controller.get_time_range(),
    )


class Filters(param.Parameterized):

    areas = param.ListSelector(
        objects=_get_unique()["areas"],
        default=[],
    )
    topics = param.ListSelector(
        objects=_get_unique()["topics"],
        default=[],
    )
    tags = param.ListSelector(
        objects=_get_unique()["tags"],
        default=[],
    )
    times = param.DateRange(
        default=_get_unique()["times"],
        softbounds=controller.get_time_range(),
        step=1000 * 60 * 60 * 24 * 5,
    )
    tasks = param.ListSelector(
        objects=_get_unique()["tasks"],
        default=[],
    )

    _data_last_loaded = datetime.now()

    def _reset_form(self):
        for param in self.param:
            if param not in ["reset_button", "reset_data_button", "name"]:
                setattr(self, param, self.param[param].default)

    def _reset_data(self):
        _get_unique.clear()
        self._data_last_loaded = datetime.now()
        for param in self.param:
            if param not in ["reset_button", "reset_data_button", "name", "times"]:
                self.param[param].objects = _get_unique()[param]

            if param == "times":
                self.param[param].softbounds = _get_unique()[param]

        self._reset_form()

    reset_button = param.Action(_reset_form, label="Reset Form")
    reset_data_button = param.Action(_reset_data, label="Reset Data")

    def __init__(self, **params):
        super().__init__(**params)

        if len(_get_unique()["topics"]) > 4:
            orientation = "vertical"
        else:
            orientation = "horizontal"

        widgets = {
            "areas": {
                "type": pn.widgets.CheckButtonGroup,
                "orientation": "horizontal",
                "button_type": "primary",
            },
            "topics": {
                "type": pn.widgets.CheckButtonGroup,
                "orientation": orientation,
                "button_type": "primary",
            },
            "tags": {
                "type": pn.widgets.CheckButtonGroup,
                "orientation": "horizontal",
                "button_type": "primary",
            },
            "times": {
                "type": pn.widgets.DatetimeRangeSlider,
                "show_value": False,
                "bar_color": "#FF0000",
                "throttled": True,
                "callback_throttle": 1000 * 2,
                "bar_color": "#428bca",
            },
            "tasks": {
                "type": pn.widgets.MultiChoice,
                "delete_button": True,
                "solid": False,
                "max_height": 500,
                "height_policy": "max",
                "option_limit": 4,
            },
            "reset_button": {
                "type": pn.widgets.Button,
                "button_type": "primary",
            },
            "reset_data_button": {
                "type": pn.widgets.Button,
                "button_type": "primary",
            },
        }
        self.controls = pn.Param(self, widgets=widgets)


FILTERS = Filters()
