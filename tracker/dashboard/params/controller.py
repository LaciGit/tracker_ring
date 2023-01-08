import param
import panel as pn

from tracker.db import Controller
from tracker.models import Area, Topic, Task, Tag

if "controller" in pn.state.cache:
    controller = pn.state.cache["controller"]
else:
    pn.state.cache["controller"] = controller = Controller()


class ParamArea(param.Parameterized):
    def save(self):
        if self.area_name:
            new_area = Area(name=self.area_name)
            controller.post(new_area)
        else:
            return pn.state.notifications.error(
                "Area name must not be empty", duration=0
            )

    area_name = param.String()
    save_button = param.Action(save, label="Save Area")

    def __init__(self, **params):
        super().__init__(**params)

        widgets = {
            "area_name": {
                "name": "Name of the area:",
                "type": pn.widgets.input.TextAreaInput,
                "placeholder": "my_area",
            },
            "save_button": {
                "type": pn.widgets.Button,
                "button_type": "primary",
            },
        }
        self.controls = pn.Param(self, widgets=widgets)


AREA = ParamArea()
