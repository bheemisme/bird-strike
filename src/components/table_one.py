from dash import Dash, dcc, html
from ..data.source import DataSource
from ..data.charts import plot_table_one, plot_table_two
from . import ids


def render(app: Dash, source: DataSource) -> html.Div:

    return html.Div(
        dcc.Graph(figure=plot_table_one(source)),
        id=ids.TABLE_ONE,
        className='w-50'
    )
