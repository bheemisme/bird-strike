from dash import Dash, dcc, html
from ..data.source import DataSource
from ..data.charts import plot_aircraft_size
from . import ids


def render(app: Dash, source: DataSource) -> html.Div:

    return html.Div(
        dcc.Graph(figure=plot_aircraft_size(source)),
        id=ids.AIRCRAFT_SIZE
    )
