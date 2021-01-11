import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from data import daily_totals_df, daily_countries_df, dropdown_options, make_global_df, make_country_df
from builders import make_table, make_bubble_map, make_bars, make_lines

countries_df = daily_countries_df()
countries = dropdown_options(countries_df)

stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
    "https://fonts.googleapis.com/css2?family=Open+Sans&display=swap"
]

app = dash.Dash(__name__, external_stylesheets=stylesheets)

server = app.server

bubble_map = make_bubble_map(countries_df)

bubble_map.update_layout(
    margin=dict(l=0, r=0, t=50, b=0), coloraxis_colorbar=dict(xanchor="left", x=0)
)

totals_df = daily_totals_df()

bars_graph = make_bars(totals_df)

bars_graph.update_traces(
    marker_color=["#e74c3c", "#8e44ad", "#27ae60"]
)

app.layout = html.Div(
    style={
        "textAlign": "center",
        "minHeight": "100vh",
        "backgroundColor": "#111111",
        "color": "white",
        "fontFamily": "Open Sans, sans-serif"
    },
    children=[
        html.Header(
            style={"textAlign": "center",
                   "paddingTop": "50px", "marginBottom": 100},
            children=[html.H1("Corona Dashboard", style={"fontSize": 40})]
        ),
        html.Div(
            style={"display": "grid", "gap": 50,
                   "gridTemplateColumns": "repeat(4, 1fr)"},
            children=[
                html.Div(
                    style={"grid-column": "span 3"},
                    children=[
                        dcc.Graph(id="bubble-map", figure=bubble_map)
                    ]
                ),
                html.Div(
                    children=[
                        make_table(countries_df),
                    ]
                ),
            ]
        ),
        html.Div(
            style={"display": "grid", "gap": 50,
                   "gridTemplateColumns": "repeat(4, 1fr)"},
            children=[
                html.Div(
                    children=[
                        dcc.Graph(id="bar-chart", figure=bars_graph)
                    ]
                ),
                html.Div(
                    style={"grid-column": "span 3"},
                    children=[
                        dcc.Dropdown(
                            style={
                                "width": 320,
                                "margin": "0 auto",
                                "color": "#111111"
                            },
                            placeholder="Select a Country",
                            id="country",
                            options=[
                                {"label": country, "value": country}
                                for country in countries
                            ]
                        ),
                        dcc.Graph(id="country_graph")
                    ]
                )
            ]
        ),
    ]
)


@app.callback(
    Output("country_graph", "figure"),
    [
        Input("country", "value")
    ]
)
def update_hello(value):
    if value is None:
        df = make_global_df()
    else:
        df = make_country_df(value)

    lines_graph = make_lines(df)
    lines_graph.update_xaxes(rangeslider_visible=True)
    lines_graph["data"][0]["line"]["color"] = "#e74c3c"
    lines_graph["data"][1]["line"]["color"] = "#8e44ad"
    lines_graph["data"][2]["line"]["color"] = "#27ae60"
    return lines_graph


# if __name__ == '__main__':
#     app.run_server(debug=True)
