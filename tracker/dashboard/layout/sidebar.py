import panel as pn

from tracker import __version__
from tracker.dashboard import FILTERS, PLOT_VIEW

pn.extension()
pn.extension(sizing_mode="stretch_width")


filters = pn.Column(
    pn.pane.Markdown("# Filter"),
    FILTERS.controls,
)

SIDEBAR = pn.GridSpec(nrows=9, width=330, height=800)

SIDEBAR[:1, 0] = PLOT_VIEW.controls
SIDEBAR[1:, 0] = FILTERS.controls
