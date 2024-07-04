from dash import Dash, html
from ..data.source import DataSource

from src.components import \
    (
        actual_strikes_year,
        phase_damage,
        table_one,
        wildlife_size_nbr_struck_actual,
        damaged_pie,
        any_cost,
        aircraft_size,
        table_two
    )


def create_layout(app: Dash, source: DataSource) -> html.Div:

    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title, className="text-center text-primary"),
            html.Div(className="body-container px-sm py-md", children=[
                html.Nav(className="navbar d-flex flex-row justify-content-around align-items-center",
                         children=[
                             #  html.Span("Navbar", className="nav-item"),
                         ]),
                html.Div(className="chart-container d-flex flex-md-row align-items-center flex-wrap flex-column",
                         children=[
                             actual_strikes_year.render(app, source),
                             phase_damage.render(app, source),
                             wildlife_size_nbr_struck_actual.render(
                                 app, source),
                             damaged_pie.render(app, source),
                             any_cost.render(app, source),
                             aircraft_size.render(app, source),
                             table_one.render(app, source),
                             table_two.render(app, source)
                         ])
            ])
        ],
    )
