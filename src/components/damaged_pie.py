from dash import Dash, dcc, html
from ..data.source import DataSource
from ..data.charts import plot_damaged_pie
from . import ids


def render(app: Dash, source: DataSource) -> html.Div:

    return html.Div(
        dcc.Graph(figure=plot_damaged_pie(source)),
        id=ids.DAMAGED_PIE,
        className="w-50",
        
    )
