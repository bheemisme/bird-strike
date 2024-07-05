from dash import Dash, dcc, html, Input, Output, callback
from ..data.source import DataSource
from ..data.charts import plot_phase_damage
from ..data.loader import DataSchema
from typing import Literal

from . import ids


def render(app: Dash, source: DataSource) -> html.Div:

    return html.Div(dcc.Graph(
        figure=plot_phase_damage(source)),
        id=ids.PHASE_DAMAGE,
        className='w-50'
    )
