
from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP
from src.components.layout import create_layout

from src.data.loader import load_data
from src.data.source import DataSource

DATA_PATH = "./data/data.csv"


def main() -> None:
    app = Dash(external_stylesheets=[BOOTSTRAP])

    data = load_data(DATA_PATH)
    data = DataSource(data)

    app.title = "Bird Strike Dashboard"
    app.layout = create_layout(app, data)
    app.run(debug=True,port="8080")


if __name__ == "__main__":
    main()
    