import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from data import daily_totals_df, daily_countries_df
from builders import make_table

countries_df = daily_countries_df()

stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
    "https://fonts.googleapis.com/css2?family=Open+Sans&display=swap"
]

app = dash.Dash(__name__, external_stylesheets=stylesheets)

bubble_map = px.scatter_geo(
    countries_df,
    title="Confirmed By Country",
    color="Confirmed",
    color_continuous_scale=px.colors.sequential.Oryel,
    size="Confirmed",
    size_max=40,
    template="plotly_dark",
    hover_name="Country_Region",
    hover_data={
        "Confirmed": ":,2f",
        "Deaths": ":,2f",
        "Recovered": ":,2f",
        "Country_Region": False
    },
    locations="Country_Region",
    locationmode="country names")

bubble_map.update_layout(
    margin=dict(l=0, r=0, t=50, b=0)
)

totals_df = daily_totals_df()

bars_graph = px.bar(
    totals_df,
    x="condition",
    y="count",
    title="Total Global Cases",
    template="plotly_dark",
    hover_data={
        "count": ":,",
        "condition": False
    },
    labels={
        "condition": "Condition",
        "count": "Count",
        "color": "Condition"
    }
)

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
                        make_table(countries_df)
                    ]
                ),
            ]
        ),
        html.Div(
            style={"display": "grid", "gap": 50,
                   "gridTemplateColumns": "repeat(4, 1fr)"},
            children=[
                dcc.Graph(id="bar-chart", figure=bars_graph)
            ]
        ),
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
