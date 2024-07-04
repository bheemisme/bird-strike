from dash import Dash, dcc, html
from ..data.source import DataSource
from ..data.charts import plot_actual_strikes_per_year
from . import ids


def render(app: Dash, source: DataSource) -> html.Div:

    return html.Div(
        dcc.Graph(figure=plot_actual_strikes_per_year(source)),
        id=ids.ACTUAL_STRIKES_YEAR,
        className="w-50"
    )
