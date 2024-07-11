from dash import Dash, dcc, html
from ..data.source import DataSource
from ..data.charts import plot_average_strike_height
from . import ids


def render(app: Dash, source: DataSource) -> html.Div:

    return html.Div(
        dcc.Graph(figure=plot_average_strike_height(source)),
        id=ids.AVERAGE_HEIGHT_WILDLIFE,
        className='w-50'
    )
