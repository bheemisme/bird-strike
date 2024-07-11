from dash import Dash, dcc, html
from ..data.source import DataSource
from ..data.charts import plot_heights
from . import ids


def render(app: Dash, source: DataSource) -> html.Div:

    return html.Div(
        dcc.Graph(figure=plot_heights(source)),
        id=ids.HEIGHTS,
        className='w-100'
    )