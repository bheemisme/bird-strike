from dash import Dash, html, register_page
from src.data.source import DataSource

from src.components import \
    (
        average_height_wildlife,
        avg_height_table,
        top_airlines,
        top_airports
    )


def create_layout(app: Dash, source: DataSource) -> html.Div:
    layout = html.Div(
        className="home-div",
        children=[
            html.Div(className="body-container px-sm py-md", children=[
                html.Div(className="chart-container d-flex flex-md-row align-items-center flex-wrap flex-column",
                         children=[
                             average_height_wildlife.render(app, source),
                             avg_height_table.render(app, source),
                             top_airlines.render(app, source),
                             top_airports.render(app, source),

                         ])
            ])
        ],
    )

    return layout
