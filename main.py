from dash import Dash, html, Input, Output, dcc
from dash_bootstrap_components.themes import BOOTSTRAP

from src.data.loader import load_data
from src.data.source import DataSource
from src.pages import home, tables, summary

DATA_PATH = "./data/data.xlsx"


def main():
    app = Dash(external_stylesheets=[BOOTSTRAP], title="Bird Strike Dashboard")

    data = load_data(DATA_PATH)
    data = DataSource(data)

    app.layout = html.Div(
        className="app-div",
        children=[
            dcc.Location(id='url', refresh=False),
            html.H1(app.title,
                    className="text-center text-primary"
                    ),
            html.Nav(
                className="navbar",
                children=[
                    dcc.Link("home", href="/",
                             className='nav-link'),
                    dcc.Link("tables", href="/tables",
                             className='nav-link'),
                    dcc.Link("summary", href="/summary",
                             className='nav-link'),
                ]
            ),
            html.Div(id="page-content")
        ]
    )

    @app.callback(
        Output('page-content', 'children'),
        [Input('url', 'pathname')]
    )
    def display_page(pathname):
        if pathname == '/':
            return home.create_layout(app, data)
        elif pathname == '/tables':
            return tables.create_layout(app, data)
        elif pathname == '/summary':
            return summary.create_layout(app, data)

    app.run(debug=True, port="8080")


if __name__ == '__main__':
    main()
