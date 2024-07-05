from dash import Dash, html, register_page
from src.data.source import DataSource

from src.components import \
    (
        table_one,
        table_two,
    )



def create_layout(app: Dash, source: DataSource) -> html.Div:
    layout = html.Div(
        className="home-div",
        children=[
            html.Div(className="body-container px-sm py-md", children=[
                html.Div(className="chart-container d-flex flex-md-row align-items-center flex-wrap flex-column",
                         children=[
                             table_one.render(app, source),
                             table_two.render(app, source),
                         ])
            ])
        ],
    )

    return layout
