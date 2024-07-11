from dash import Dash, dcc, html
from ..data.source import DataSource
from ..data.charts import plot_yearly_cost
from . import ids


def render(app: Dash, source: DataSource) -> html.Div:

    return html.Div(
        dcc.Graph(figure=plot_yearly_cost(source)),
        id=ids.TOP_AIRPORTS,
        className='w-50'
    )
