# ========== (c) JP Hwang 5/8/2022  ==========

import logging

# ===== START LOGGER =====
logger = logging.getLogger(__name__)

import pandas as pd
import numpy as np
import dash
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

desired_width = 320
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', desired_width)

# DBC themes: https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/
app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.BOOTSTRAP,  # DBC themes: https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/
    {
        'href': 'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf',
        'crossorigin': 'anonymous'
    }
])

server = app.server

publications = []

# DASH LAYOUT
header = html.Div([
    dbc.Container([
        html.Header(html.H5("Dash + Weaviate | Starter App".upper(), className="fs-4"), className="d-flex flex-wrap justify-content-center my-1 pb-1 border-bottom")
    ]),
    dbc.Container([
        html.H4([html.I(className="fas fa-taxi rounded text-warning py-1 px-1 mr-2"), html.Span(["NYC Taxi".upper()], className="text-warning"), " Data Dashboard".upper()], className="display-5 fw-bold mt-3"),
        html.Div([
            html.P([
                "This dashboard leverages ", html.A("Weaviate", href="https://weaviate.io/"), " with ", html.A("Plotly Dash", href="https://dash.plotly.com/"),
                " to show how quickly and easily powerful, scalable vector search engines can be built to improve your knowledge management.",
            ], className="lead mb-1"),
        ]),
    ])
], className="bg-dark text-light my-0 py-4")

body = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    html.H4("Controls", className="display-5 fw-bold lh-1 mb-3 pb-2 border-bottom"),
                    html.Div([
                        html.H6([html.I(className="fas fa-map-pin rounded text-dark py-1 px-2 mr-2"), "FILTER: By boroughs".upper()]),
                        dcc.Dropdown(
                            id='publication',
                            options=[{"label": b, "value": b} for b in publications],
                            multi=True,
                            value=publications[0]
                        ),
                    ])
                ], className='bg-light p-3')
            ], sm=12, md=4, className="mr-3"),
            dbc.Col([
                html.H4("Outputs", className="display-5 fw-bold lh-1 mb-3 pb-2 border-bottom"),
                html.H5([html.I(className="fas fa-clock rounded bg-primary text-white py-1 px-1 mr-2"), "Pickups by time of the day".upper()], className="mt-2"),
                dcc.Graph(figure=px.bar(), id="bar-fig"),
                html.H5([html.I(className="fas fa-chart-line rounded bg-primary text-white py-1 px-1 mr-2"), "Explore correlations".upper()], className="mt-3"),
                dbc.Row([
                    dbc.Col([
                        dcc.Dropdown(
                            id='var-x',
                            options=[{"label": v, "value": k} for k, v in var_x_dict.items()],
                            value="trip_distance"
                        ),
                    ], className="sm-6"),
                    dbc.Col([
                        dcc.Dropdown(
                            id='var-y',
                            options=[{"label": v, "value": k} for k, v in var_y_dict.items()],
                            value="fare_amount"
                        ),
                    ], className="sm-6"),
                ]),
                dcc.Graph(figure=px.scatter(), id="scatter-fig")
            ], sm=12, md=7, className="p-3"),
        ], className="g-5 py-5 mt-2"),
        html.Div([
            html.A([html.Img(src="assets/logo-plotly.svg", className="mr-2", height="30px")], href="https://plotly.com/"),
            html.A([html.Img(src="assets/logo-coiled.svg", className="mr-2", height="50px")], href="https://coiled.io/"),
            html.P(html.Small(["Dataset from ", html.A("TLC Trip Record Data", href="https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page"), "."])),
        ]),
    ])
])

app.layout = html.Div([header, body])

if __name__ == '__main__':
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    sh.setFormatter(formatter)
    root_logger.addHandler(sh)

    app.run_server(debug=True)
