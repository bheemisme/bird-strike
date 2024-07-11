from dash import Dash, dcc, html
from ..data.source import DataSource
from ..data.charts import plot_effect_impact
from . import ids


def render(app: Dash, source: DataSource) -> html.Div:

    return html.Div(
        dcc.Graph(figure=plot_effect_impact(source)),
        id=ids.EFFECT_IMPACT,
        className='w-100'
    )
