from dash import Dash, dcc, html
from ..data.source import DataSource
from ..data.charts import plot_avg_height_table
from . import ids


def render(app: Dash, source: DataSource) -> html.Div:

    return html.Div(
        dcc.Graph(figure=plot_avg_height_table(source)),
        id=ids.AVERAGE_HEIGHT_TABLE,
        className='w-50'
    )
