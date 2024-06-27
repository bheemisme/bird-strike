from dash import Dash, html
from ..data.source import DataSource



def create_layout(app: Dash, source: DataSource) -> html.Div:

    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title, className="text-center text-primary"),
            html.Div(className="body-container px-sm py-md", children=[
                html.Nav(className="navbar d-flex flex-row justify-content-around align-items-center",
                         children=[
                             html.Span("Navbar", className="nav-item"),
                         ]),
                html.Div(className="chart-container d-flex flex-row align-items-center flex-wrap",
                         children=[
                             
                         ])
            ])
        ],
    )