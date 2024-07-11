from dash import Dash, dcc, html
from ..data.source import DataSource
from . import ids


def render() -> html.Nav:

    return html.Nav(
        className="navbar",
        children=[
            dcc.Link("home", href="/",
                     className='nav-link'),
            dcc.Link("tables", href="/tables",
                     className='nav-link'),
            dcc.Link("summary", href="/summary",
                     className='nav-link'),
        ]
    )
