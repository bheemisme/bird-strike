from dash import Dash, dcc, html
from ..data.source import DataSource
from ..data.charts import plot_heights_histogram
from . import ids


def render(app: Dash, source: DataSource) -> html.Div:

    return html.Div(
        dcc.Graph(figure=plot_heights_histogram(source)),
        id=ids.HEIGHTS_HIST,
        className='w-50'
    )
