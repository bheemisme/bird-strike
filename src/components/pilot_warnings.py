from dash import Dash, dcc, html
from ..data.source import DataSource
from ..data.charts import plot_pilot_warnings
from . import ids


def render(app: Dash, source: DataSource) -> html.Div:

    return html.Div(
        dcc.Graph(figure=plot_pilot_warnings(source)),
        id=ids.PILOTS_WARNINGS,
        className='w-100'
    )
