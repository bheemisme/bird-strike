from dash import Dash, dcc, html
from ..data.source import DataSource
from ..data.charts import plot_aircraft_altitude
from . import ids


def render(app: Dash, source: DataSource) -> html.Div:

    return html.Div(
        dcc.Graph(figure=plot_aircraft_altitude(source)),
        id=ids.AIRCRAFT_ALTITUDE,
        className="w-100"
    )
