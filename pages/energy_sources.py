from dash import html, dcc, Input, Output, callback, register_page
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from config import SOURCE_COLORS, SOURCE_LABELS


register_page(__name__, top_nav=True)

# -----
# Setup
# -----

df = pd.read_csv("data/ura-market-snapshots.csv", thousands=",")
# Update 'Malekula' location to use more accurate location name to match later reports
df.loc[df["location"] == "Malekula", "location"] = "Malekula- Lakatoro"
# TODO percent renewable or something by location (map view?) 3D map view?

DATES = sorted(list(set(df["date"].values)))
LOCATIONS = ["Vanuatu"] + list(set(df["location"].values))


def build_line_chart(location: str = "Vanuatu"):
    figure = go.Figure()
    figure.update_yaxes(title_text="kWh Produced")
    for source, color in zip(SOURCE_LABELS, SOURCE_COLORS):
        legendgroup = "non-renewable" if source == "diesel" else "renewable"
        y = []
        for date in DATES:
            data = df.query(f"source=='{source}' & date=='{date}'")
            if location != "Vanuatu":
                data = data.query(f"location=='{location}'")
            y.append(data["kwh"].sum())
        figure.add_trace(
            go.Scatter(
                name=source,
                x=DATES,
                y=y,
                line=dict(width=2, color=color),
                stackgroup="one",
                legendgroup=legendgroup,
                legendgrouptitle_text=legendgroup.title(),
                hoverinfo="x+y+name",
            )
        )
    figure.update_layout(legend=dict(groupclick="toggleitem"))
    # TODO just make notes in text - I don't want too many of these to manage
    # if location in ["Vanuatu", "Port Vila"]:
    #     fig.add_annotation(
    #         x="2020-05",
    #         y=3_700_000,
    #         text="Copra oil stopped in Port Vila",
    #         showarrow=True,
    #         yshift=10,
    #     )
    return figure


def build_pie_chart(location: str, date):
    data = df.query(f"date=='{date}'")
    if location != "Vanuatu":
        data = data.query(f"location=='{location}'")
    values = [data.query(f"source=='{s}'")["kwh"].sum() for s in SOURCE_LABELS]
    figure = go.Figure(
        data=[
            go.Pie(
                labels=SOURCE_LABELS,
                values=values,
                marker_colors=SOURCE_COLORS,
                pull=[0.2, 0, 0, 0, 0],
            )
        ]
    )
    figure.update_layout(legend=dict(groupclick="toggleitem"))
    return figure


def build_renewable_percent_chart(location: str = "Vanuatu"):
    values = []
    for date in DATES:
        renewable = 0
        nonrenewable = 0
        if location != "Vanuatu":
            data = df.query(f"date=='{date}' & location=='{location}'")
        else:
            data = df.query(f"date=='{date}'")
        for source in SOURCE_LABELS:
            subtotal = data.loc[data["source"] == source]["kwh"].sum()
            if source == "diesel":
                nonrenewable = subtotal
            else:
                renewable += subtotal
        total_production = renewable + nonrenewable
        renewable_percent = renewable / total_production
        values.append((date, renewable_percent))
    
    renewable_df = pd.DataFrame(values, columns=["date", "percent"])
    figure = px.area(renewable_df, x="date", y="percent")
    figure.update_layout(yaxis_title="Percent Renewable Energy Produced")
    figure.update_yaxes(range=[0, 1])
    figure.for_each_trace(lambda trace: trace.update(fillcolor = SOURCE_COLORS[1]))
    figure.for_each_trace(lambda trace: trace.line.update(color = SOURCE_COLORS[2]))
    return figure


figure = build_line_chart()
figure2 = build_renewable_percent_chart()

# ------
# Layout
# ------

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


layout = html.Div(
    [
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
        dbc.Row(
            [
                dcc.Graph(id="graphA", figure=figure2),
            ]
        ),
    ]
)


@callback(
    Output("graph", "figure"),
    Output("graphA", "figure"),
    [
        Input("location-select", "value"),
        Input("date-select", "value"),
    ],
)
def update_figure_location(location, date):
    if date is None:
        fig = build_line_chart(location)
        fig2 = build_renewable_percent_chart(location)
    else:
        fig = build_pie_chart(location, date)
        fig2 = build_renewable_percent_chart(location)
    return fig, fig2
