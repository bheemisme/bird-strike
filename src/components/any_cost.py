from dash import Dash, dcc, html
from ..data.source import DataSource
from ..data.charts import plot_damage_any_cost
from . import ids


def render(app: Dash, source: DataSource) -> html.Div:

    return html.Div(
        dcc.Graph(figure=plot_damage_any_cost(source)),
        id=ids.ANY_COST
    )
