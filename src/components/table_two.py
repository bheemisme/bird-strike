from dash import Dash, dcc, html
from ..data.source import DataSource
from ..data.charts import plot_table_two
from . import ids


def render(app: Dash, source: DataSource) -> html.Div:

    return html.Div(
        dcc.Graph(figure=plot_table_two(source)),
        id=ids.TABLE_TWO,
        className='w-50'
    )
