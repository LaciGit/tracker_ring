from datetime import datetime
import param
import panel as pn

from tracker.db import Controller
from tracker.models import Area, Topic, Task, Tag

if "controller" in pn.state.cache:
    controller = pn.state.cache["controller"]
else:
    pn.state.cache["controller"] = controller = Controller()


@pn.cache
def _get_unique():
    return dict(
        areas=controller.get_unique("area"),
        topics=controller.get_unique("topic"),
        tasks=controller.get_unique("task"),
        tags=controller.get_unique("tag"),
        times=controller.get_time_range(),
    )


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


class ParamTag(param.Parameterized):
    def save(self):
        if self.tag_name:
            new_tag = Tag(name=self.tag_name)
            controller.post(new_tag)
        else:
            return pn.state.notifications.error(
                "Tag name must not be empty", duration=0
            )

    tag_name = param.String()
    save_button = param.Action(save, label="Save Tag")

    def __init__(self, **params):
        super().__init__(**params)

        widgets = {
            "tag_name": {
                "name": "Name of the tag:",
                "type": pn.widgets.input.TextAreaInput,
                "placeholder": "my_tag",
            },
            "save_button": {
                "type": pn.widgets.Button,
                "button_type": "primary",
            },
        }
        self.controls = pn.Param(self, widgets=widgets)


class ParamTopic(param.Parameterized):
    def save(self):
        if self.topic_name:
            new_topic = Topic(name=self.topic_name, bookingNumber=self.booking_number)
            controller.post(new_topic)
            area = controller.get(cls="Area", name=self.map_to_area)
            controller.update_by_child(parent=area, child=new_topic)

        else:
            return pn.state.notifications.error(
                "Topic name must not be empty", duration=0
            )

    topic_name = param.String()
    booking_number = param.String()
    map_to_area = param.Selector(objects=controller.get_unique("area"))
    save_button = param.Action(save, label="Save Topic")

    def __init__(self, **params):
        super().__init__(**params)

        widgets = {
            "topic_name": {
                "name": "Name of the topic:",
                "type": pn.widgets.input.TextAreaInput,
                "placeholder": "my_topic",
            },
            "booking_number": {
                "name": "Booking number:",
                "type": pn.widgets.input.TextAreaInput,
                "placeholder": "AFE ...",
            },
            "map_to_area": {
                "type": pn.widgets.RadioButtonGroup,
                "orientation": "horizontal",
                "button_type": "primary",
            },
            "save_button": {
                "type": pn.widgets.Button,
                "button_type": "primary",
            },
        }
        self.controls = pn.Param(self, widgets=widgets)


class ParamTask(param.Parameterized):
    def save(self):

        if self.task_name:
            task_name = self.task_name.strip()
        else:
            task_name = self.task_name_pre.strip()

        if task_name:
            list_tags_id = [
                controller.get(cls="Tag", name=t).id for t in self.map_to_tags
            ]
            datetime.combine(self.time, datetime.min.time())
            new_task = Task(
                name=task_name,
                tags=list_tags_id,
                duration=self.duration,
                time=datetime.combine(self.time, datetime.min.time()),
            )
            controller.post(new_task)

            topic = controller.get(cls="Topic", name=self.map_to_topic)
            controller.update_by_child(parent=topic, child=new_task)

            return pn.state.notifications.success(
                f"Task '{new_task.name}' was successfully saved!", duration=10 * 1000
            )

        else:
            return pn.state.notifications.error(
                "Task name must not be empty", duration=0
            )

    task_name = param.String()
    task_name_pre = param.Selector(
        objects=controller.get_unique("task"),
        default=controller.get_unique("task")[0],
    )
    duration = param.Integer(default=15, bounds=(5, 60 * 4), step=5)
    time = param.Date(datetime.now().date())
    map_to_topic = param.Selector(objects=controller.get_unique("topic"))
    map_to_tags = param.ListSelector(objects=controller.get_unique("tag"), default=[])
    save_button = param.Action(save, label="Save Task")

    def __init__(self, **params):
        super().__init__(**params)

        widgets = {
            "duration": {
                "name": "Duration of the task",
                "type": pn.widgets.IntSlider,
                "bar_color": "#428bca",
            },
            "task_name_pre": {
                "name": "Name of the task (if input empty):",
                "type": pn.widgets.Select,
            },
            "task_name": {
                "name": "Name of the task:",
                "type": pn.widgets.input.TextAreaInput,
                "placeholder": "my_task",
            },
            "map_to_topic": {
                "type": pn.widgets.RadioButtonGroup,
                "orientation": "horizontal",
                "button_type": "primary",
            },
            "save_button": {
                "type": pn.widgets.Button,
                "button_type": "primary",
            },
            "map_to_tags": {
                "type": pn.widgets.CheckButtonGroup,
                "orientation": "horizontal",
                "button_type": "primary",
            },
            "time": {"type": pn.widgets.DatePicker},
        }
        self.controls = pn.Param(self, widgets=widgets)


AREA = ParamArea()
TOPIC = ParamTopic()
TASK = ParamTask()
TAG = ParamTag()
