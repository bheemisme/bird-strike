from dash import Dash, dcc, html
from ..data.source import DataSource
from ..data.charts import plot_wildlife_size_nbr_struck_actual
from . import ids


def render(app: Dash, source: DataSource) -> html.Div:

    return html.Div(
        dcc.Graph(figure=plot_wildlife_size_nbr_struck_actual(source)),
        id=ids.SIZE_STRUCK_ACTUAL,
        className="w-50"
    )
