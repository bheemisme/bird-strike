from dash import Dash, dcc, html
from ..data.source import DataSource
from ..data.charts import plot_top_fifty_airports
from . import ids


def render(app: Dash, source: DataSource) -> html.Div:

    return html.Div(
        dcc.Graph(figure=plot_top_fifty_airports(source)),
        id=ids.TOP_AIRPORTS,
        className='w-50'
    )
