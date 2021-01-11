import dash_html_components as html
import plotly.express as px


def make_lines(df):
    return px.line(
        df,
        x="date",
        y=["confirmed", "deaths", "recovered"],
        template="plotly_dark",
        labels={
            "value": "Cases",
            "variable": "Condition",
            "date": "Date",
        },
        hover_data={
            "value": ":,",
            "variable": False,
            "date": False
        })


def make_bars(df):
    return px.bar(
        df,
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
        })


def make_bubble_map(df):
    return px.scatter_geo(
        df,
        title="Confirmed By Country",
        color="Confirmed",
        projection="equirectangular",
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


def make_table(df):
    return html.Table(
        children=[
            html.Thead(
                style={"display": "block", "marginBottom": 25},
                children=[
                    html.Tr(
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "repeat(4, 1fr)",
                            "fontWeight": "600",
                            "fontSize": 16,
                        },
                        children=[
                            html.Th(
                                column_name.replace("_", " "))
                            for column_name in df.columns
                        ]
                    )
                ]
            ),
            html.Tbody(
                style={"maxHeight": "50vh", "display": "block",
                       "overflow": "scroll", },
                children=[
                    html.Tr(
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "repeat(4, 1fr)",
                            "border-top": "1px solid white",
                            "padding": "30px 0px",
                        },
                        children=[
                            html.Td(value_column) for value_column in value
                        ]
                    ) for value in df.values
                ]
            )
        ]
    )
