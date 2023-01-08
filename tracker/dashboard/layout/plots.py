import param
import panel as pn
import hvplot.pandas
import plotly.express as px
import holoviews as hv

from plotly.graph_objects import Layout
from tracker.dashboard import DATA_HANDLER


color_map = [
    "#428bca",
    "#fd7f6f",
    "#bd7ebe",
    "#ffb55a",
    "#ffee65",
    "#beb9db",
    "#fdcce5",
    "#7eb0d5",
    "#b2e061",
    "#8bd3c7",
    "#b3d4ff",
]


pn.extension(sizing_mode="stretch_both")


class DurationPlot(param.Parameterized):
    data_handler = param.ClassSelector(
        param.Parameterized,
        DATA_HANDLER,
        instantiate=False,
    )

    @pn.depends("data_handler.param")
    def create_plot_1(self):
        df = self.data_handler._df_result

        if df.shape[0] == 0:
            return pn.pane.Alert(
                "**Error**: No data for this filter config availible!",
                alert_type="danger",
            )

        df["duration_h"] = df.duration / 60
        df["day_of_year"] = df.time.dt.day_of_year
        df["year"] = df.time.dt.isocalendar().year
        df["weekofyear"] = df.time.dt.isocalendar().week
        df["year_week"] = df.apply(lambda x: f"{x.year}-{x.weekofyear}", axis=1)

        df = df[["year_week", "duration_h", "task_name"]]

        # define how to aggregate various fields
        agg_functions = {
            "duration_h": "sum",
        }

        # create new DataFrame by combining rows with same id values
        df_new = (
            df.groupby(["task_name", "year_week"])
            .aggregate(agg_functions)
            .reset_index()
            .sort_values("year_week")
        )

        mean_duration = df_new.groupby("year_week")["duration_h"].sum().mean()

        return df_new.hvplot.bar(
            x="year_week",
            xlabel="",
            y="duration_h",
            ylabel="duration [h]",
            by="task_name",
            stacked=True,
            legend="top",
            title="Stacked duration of tasks over calendar weeks",
            alpha=0.8,
            grid=True,
            cmap={
                v: (color_map * 3)[i]
                for i, v in enumerate(
                    df.reset_index()[["task_name", "duration_h"]]
                    .groupby("task_name", dropna=False)
                    .sum()
                    .sort_values("duration_h", ascending=False)
                    .index
                )
            },
        ) * hv.HLine(mean_duration).opts(
            color="black",
            line_dash="dashed",
            line_width=2.0,
            alpha=0.2,
        )

    @pn.depends("data_handler.param")
    def create_plot_2(self):
        df = self.data_handler._df_result

        if df.shape[0] == 0:
            return pn.pane.Alert(
                "**Error**: No data for this filter config availible!",
                alert_type="danger",
            )

        df = df.dropna(axis=1, how="all")
        if not "tag_name" in df.columns:
            return pn.pane.Alert(
                "**Error**: No tags found in dataset!",
                alert_type="danger",
            )

        df[["year", "week", "day"]] = df.time.dt.isocalendar()
        df["year_week"] = df.apply(lambda x: f"{x.year}-{x.weekofyear}", axis=1)

        df_gr = df.groupby(["year_week", "tag_name"]).count()
        df_gr = df_gr.rename(columns={"task_name": "count"})
        df_gr = df_gr[["count"]]

        return df_gr.hvplot.bar(
            xlabel="",
            ylabel="",
            alpha=0.8,
            grid=True,
            title="Count of tags in given tasks over calendar weeks",
            legend="top",
            cmap={
                v: color_map[i]
                for i, v in enumerate(
                    df_gr.reset_index()[["tag_name", "count"]]
                    .groupby("tag_name")
                    .sum()
                    .sort_values("count", ascending=False)
                    .index
                )
            },
            stacked=True,
        )


class Sunburst(param.Parameterized):

    data_handler = param.ClassSelector(
        param.Parameterized,
        DATA_HANDLER,
        instantiate=False,
    )

    @pn.depends("data_handler.param")
    def create_plot(self):

        df_filter = self.data_handler._df_result[
            ["duration", "area_name", "topic_name", "task_name", "tag_name"]
        ]
        if df_filter.shape[0] == 0:
            return pn.pane.Alert(
                "**Error**: No data for this filter config availible!",
                alert_type="danger",
            )

        df_filter = df_filter.dropna(axis=1, how="all")

        cols = [
            c
            for c in df_filter.columns
            if c in ["area_name", "topic_name", "task_name", "tag_name"]
        ]
        df_filter = df_filter.groupby(by=cols, dropna=False).sum()
        df_filter = df_filter.reset_index()

        df_filter = df_filter.drop(df_filter[df_filter["duration"] == 0].index)
        df_filter["duration_%"] = round(
            (df_filter["duration"] / df_filter["duration"].sum(numeric_only=True))
            * 100,
            2,
        )
        fig = px.sunburst(
            df_filter,
            path=cols,
            values="duration",
            title="<em>Split duration into hierarchy</em>",
            color_discrete_sequence=color_map,
        )
        fig.update_layout(
            Layout(
                margin=dict(l=50, r=50, t=50, b=50),
                font={
                    "family": "Helvetica",
                    "size": 10,
                },
            )
        )
        fig.update_traces(leaf=dict(opacity=0.7))

        return pn.pane.Plotly(
            fig,
            config={"responsive": True},
        )


class KpiTags(param.Parameterized):

    data_handler = param.ClassSelector(
        param.Parameterized,
        DATA_HANDLER,
        instantiate=False,
    )

    @pn.depends("data_handler.param")
    def create_plot(self):

        df = self.data_handler._df_result[["tag_name", "topic_name", "duration"]]

        df = df.dropna(axis=1, how="all")
        if not "tag_name" in df.columns:
            return pn.pane.Alert(
                "**Error**: No tags found in dataset!",
                alert_type="danger",
            )

        df = (
            df[["tag_name", "topic_name", "duration"]]
            .groupby(["tag_name", "topic_name"])
            .count()
            .sort_values("duration", ascending=False)
            .reset_index()
            .groupby("tag_name")
            .aggregate({"topic_name": "first", "duration": "first"})
        )

        kpi_string = "\n".join(
            [
                f"- **{tag}** in {topic} = {count}"
                for tag, topic, count in zip(
                    df.index, df["topic_name"].values, df["duration"].values
                )
            ]
        )

        return pn.pane.Markdown(
            "#### Tag KPIs \n most occurrences of:\n\n" + kpi_string
        )


SUNBURST = Sunburst()
DURATION_PLTOS = DurationPlot()
KPI_TAGS = KpiTags()
