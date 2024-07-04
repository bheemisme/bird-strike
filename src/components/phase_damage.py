from dash import Dash, dcc, html
from ..data.source import DataSource
from ..data.charts import plot_phase_damage
from . import ids


def render(app: Dash, source: DataSource) -> html.Div:

    return html.Div(
        dcc.Graph(figure=plot_phase_damage(source)),
        id=ids.PHASE_DAMAGE,
        className="w-50"
    )
