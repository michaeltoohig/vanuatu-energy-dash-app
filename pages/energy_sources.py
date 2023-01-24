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
                html.H6("Location", className="text-white my-1"),
                dcc.Dropdown(
                    id="location-select",
                    options=LOCATIONS,
                    value="Vanuatu",
                    clearable=False,
                ),
            ],
            className="mb-3"
        ),
        html.Div(
            [
                html.H6("Date", className="text-white mb-0"),
                html.P("Select date to view pie chart for selected date.", className="small text-white mb-1"),
                dcc.Dropdown(
                    id="date-select",
                    options=list(reversed(DATES)),
                    value=None,
                    clearable=True,
                ),
            ],
        ),
    ],
    body=True,
    color="primary",
)

alert = dbc.Alert(
    [
        html.H4("Reports Discontinued(?)", className="alert-heading"),
        html.P(
            """
                The URA has not released a new report since March 2022 and their website
                has been offline since the Vanuatu government experienced a cyber attack
                at the end of 2022. So be aware that the charts below are not
                representative of the current state of energy sources in Vanuatu.
            """
        ),
        html.Hr(),
        html.P(
            "Please get into contact with me if you can point me to where to find new reports or why reports have stopped in 2022.",
            className="mb-0",
        ),
    ],
    color="warning",
)

layout = html.Div(
    [
        alert,
        html.H2("Energy Sources"),
        html.P(
            """
                This chart shows the amount of kilowatt/hours produced by each reported source of energy.
                Use the form below to update the charts and show the data of a specific region and/or date.
            """
        ),
        controls,
        html.Div(
            [
                html.H4("Total Production by Energy Source"),
                html.P(
                    "This chart shows amount electricity produced (measured in kwh) as well as the amount that various energy sources contribute to that demand so the relationship between them can be compared."
                ),
            ],
            className="mt-3 mb-0",
        ),
        dbc.Row(
            [
                dcc.Graph(id="graph", figure=figure),
            ]
        ),
        html.Div(
            [
                html.H4("Renewable Energy Production"),
                html.P(
                    "This chart shows percentage of electricity produced with renewable sources."
                ),
            ],
            className="mt-3 mb-0",
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
