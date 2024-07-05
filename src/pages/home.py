from dash import Dash, html
from src.data.source import DataSource

from src.components import \
    (
        actual_strikes_year,
        phase_damage,
        wildlife_size_nbr_struck_actual,
        damaged_pie,
        any_cost,
        aircraft_size
    )



def create_layout(app: Dash, source: DataSource) -> html.Div:
    
    layout = html.Div(
        className="home-div",
        children=[
            html.Div(className="body-container px-sm py-md", children=[
                html.Div(className="chart-container d-flex flex-md-row align-items-center flex-wrap flex-column",
                         children=[
                             actual_strikes_year.render(app, source),
                             phase_damage.render(app, source),
                             wildlife_size_nbr_struck_actual.render(app, source),
                             damaged_pie.render(app, source),
                             any_cost.render(app, source),
                             aircraft_size.render(app, source),
                             
                         ])
            ])
        ],
    )

    return layout
