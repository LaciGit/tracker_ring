import panel as pn

from tracker import __version__
from tracker.dashboard import FILTERS

pn.extension()
pn.extension(sizing_mode="stretch_width")


filters = pn.Column(
    pn.pane.Markdown("# Filter"),
    FILTERS.controls,
)

SIDEBAR = pn.GridSpec(nrows=9, width=300)
SIDEBAR[:, 0] = FILTERS.controls
