from dash import Dash, dcc, html
from ..data.source import DataSource
from ..data.charts import plot_phase_height
from . import ids


def render(app: Dash, source: DataSource) -> html.Div:

    return html.Div(
        dcc.Graph(figure=plot_phase_height(source)),
        id=ids.PHASE_HEIGHT,
        className='w-50'
    )
