from dash import html, dcc, Input, Output, callback, register_page
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

import pandas as pd

register_page(__name__, top_nav=True)


df = pd.read_csv("data/ura-market-snapshots.csv", thousands=",")
# Update 'Malekula' location to use more accurate location name to match later reports
df.loc[df["location"] == "Malekula", "location"] = "Malekula- Lakatoro"


DATES = sorted(list(set(df["date"].values)))
LOCATIONS = ["Vanuatu"] + list(set(df["location"].values))
SOURCES = ["diesel", "copra oil", "hydro", "solar", "wind"]
COLORS = ["#1D1E18", "#D9FFF5", "#B9F5D8", "#AAD2BA", "#6B8F71"]


figure = go.Figure()
figure.update_yaxes(title_text="kWh Produced")
for source, color in zip(SOURCES, COLORS):
    legendgroup = "non-renewable" if source == "diesel" else "renewable"
    y = []
    for date in DATES:
        data = df.query(f"source=='{source}' & date=='{date}'")
        y.append(data["kwh"].sum())
    figure.add_trace(
        go.Scatter(
            name=source,
            x=DATES,
            y=y,
            line=dict(width=2, color=color),
            stackgroup="one",
            legendgroup=legendgroup,
            hoverinfo="x+y+name",
        )
    )


controls = dbc.Card(
    [
        html.Div(
            [
                dbc.Label("Location"),
                dcc.Dropdown(
                    id="location-select",
                    options=LOCATIONS,
                    value="Vanuatu",
                    clearable=False,
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("Date"),
                dcc.Dropdown(
                    id="date-select",
                    options=list(reversed(DATES)),
                    value=None,
                    clearable=True,
                ),
                html.P("Select date to view pie chart"),
            ]
        ),
    ],
    body=True,
)


layout = html.Div([
    html.H2("Energy Sources"),
    html.P(
        "This chart shows the amount of kilowatts/hours produced by each reported source of energy."
    ),
    dbc.Row([dbc.Col(controls)]),
    dbc.Row(
        [
            dcc.Graph(id="graph", figure=figure),
        ]
    ),
])



@callback(
    Output("graph", "figure"),
    [
        Input("location-select", "value"),
        Input("date-select", "value"),
    ],
)
def update_figure_location(location, date):
    if date is None:
        fig = go.Figure()
        fig.update_yaxes(title_text="kWh Produced")
        for source, color in zip(SOURCES, COLORS):
            legendgroup = "non-renewable" if source == "diesel" else "renewable"
            y = []
            for date in DATES:
                data = df.query(f"source=='{source}' & date=='{date}'")
                if location != "Vanuatu":
                    data = data.query(f"location=='{location}'")
                y.append(data["kwh"].sum())
            fig.add_trace(
                go.Scatter(
                    name=source,
                    x=DATES,
                    y=y,
                    line=dict(width=2, color=color),
                    stackgroup="one",
                    legendgroup=legendgroup,
                    hoverinfo="x+y+name",
                )
            )
            # TODO just make notes in text - I don't want too many of these to manage
            # if location in ["Vanuatu", "Port Vila"]:
            #     fig.add_annotation(
            #         x="2020-05",
            #         y=3_700_000,
            #         text="Copra oil stopped in Port Vila",
            #         showarrow=True,
            #         yshift=10,
            #     )
    else:
        data = df.query(f"date=='{date}'")
        if location != "Vanuatu":
            data = data.query(f"location=='{location}'")
        values = [data.query(f"source=='{s}'")["kwh"].sum() for s in SOURCES]
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=SOURCES,
                    values=values,
                    marker_colors=COLORS,
                    pull=[0.2, 0, 0, 0, 0],
                )
            ]
        )
    return fig