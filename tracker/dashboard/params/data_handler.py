import param
import panel as pn

from datetime import datetime
from tracker.db import Controller
from tracker.dashboard import FILTERS

pn.extension()
pn.extension(sizing_mode="stretch_width")

if "controller" in pn.state.cache:
    controller = pn.state.cache["controller"]
else:
    pn.state.cache["controller"] = controller = Controller()


@pn.cache
def _pull_data():
    return controller.get_df(clean_ids=True)


class DataHandler(param.Parameterized):

    filter = param.ClassSelector(param.Parameterized, FILTERS, instantiate=False)

    _df_original = _pull_data()
    _data_last_loaded = datetime.now()
    _df_result = param.DataFrame(default=_df_original)

    @param.depends("filter.param", watch=True)
    def _reload_data(self):
        if self.filter._data_last_loaded > self._data_last_loaded:
            self._data_last_loaded = self.filter._data_last_loaded
            print("reloaded data")
            _pull_data.clear()
            self._df_original = _pull_data()

    @param.depends("filter.param", watch=True)
    def _update_data(self):
        query = []
        if areas := self.filter.areas:
            query.append("(area_name in @areas)")
        if topics := self.filter.topics:
            query.append("(topic_name in @topics)")
        if tasks := self.filter.tasks:
            query.append("(task_name in @tasks)")
        if tags := self.filter.tags:
            query.append("(tag_name in @tags)")

        time_from = self.filter.times[0]
        time_to = self.filter.times[1]

        query.append("((time >= @time_from) & time <= @time_to )")

        if query:
            self._df_result = self._df_original.query(" & ".join(query)).copy(deep=True)
        else:
            self._df_result = self._df_original


DATA_HANDLER = DataHandler()
