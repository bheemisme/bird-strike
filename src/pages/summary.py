from dash import Dash, html
from src.data.source import DataSource

from src.components import \
    (
        costs_hist,
        heights_hist,
        engines_pie,
        heights,
        yearly_costs,
        phase_height,
        effect_impact,
        aircraft_altitude,
        strike_altitude
    )


def create_layout(app: Dash, source: DataSource) -> html.Div:
    layout = html.Div(
        className="home-div",
        children=[
            html.Div(className="body-container px-sm py-md", children=[
                html.Div(className="chart-container d-flex flex-md-row align-items-center flex-wrap flex-column",
                         children=[
                             costs_hist.render(app, source),
                             heights_hist.render(app, source),
                             engines_pie.render(app, source),
                             heights.render(app, source),
                             yearly_costs.render(app, source),
                             phase_height.render(app, source),
                             effect_impact.render(app, source),
                             aircraft_altitude.render(app, source),
                             strike_altitude.render(app, source)
                         ])
            ])
        ],
    )

    return layout
