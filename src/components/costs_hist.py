from dash import Dash, dcc, html
from ..data.source import DataSource
from ..data.charts import plot_costs_histogram
from . import ids


def render(app: Dash, source: DataSource) -> html.Div:

    return html.Div(
        dcc.Graph(figure=plot_costs_histogram(source)),
        id=ids.COSTS_HIST, 
        className='w-50'
    )