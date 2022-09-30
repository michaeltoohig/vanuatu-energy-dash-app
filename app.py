from datetime import datetime
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd

DESCRIPTION = "An open source dashboard on Vanuatu's eneregy sources and prices from information obtained in public records."

app = Dash(
    __name__,
    title="Vanuatu Energy Dashboard",
    meta_tags=[
        {
            "name": "description",
            "content": DESCRIPTION,
        },
    ],
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

server = app.server

df = pd.read_csv("ura-market-snapshots.csv", thousands=",")
# Update 'Malekula' location to use more accurate location name to match later reports
df.loc[df["location"] == "Malekula", "location"] = "Malekula- Lakatoro"
unelco_rates = pd.read_csv("electricity.csv")
oil_prices = pd.read_csv("data/crudoil-wti.csv")
# Update date value to remove day from date
oil_prices["date"] = oil_prices["date"].str.replace("-15", "")
exchange_rates = pd.read_csv("data/exchange-rates/monthly.csv")
# Update USD/barrel price to Vatu/barrel price by exchante rate of same month
oil_prices = pd.concat(
    [
        oil_prices.set_index("date"),
        exchange_rates.set_index("date"),
    ],
    axis=1,
    join="inner",
).reset_index()
oil_prices.loc[:, ["price"]] = oil_prices.loc[:, ["price"]].divide(
    oil_prices.loc[:, "exchange_rate"],
    axis="index",
)
oil_prices["price"] = oil_prices["price"].astype("int")


DATES = sorted(list(set(df["date"].values)))
LOCATIONS = ["Vanuatu"] + list(set(df["location"].values))
SOURCES = ["diesel", "copra oil", "hydro", "solar", "wind"]
COLORS = ["#1D1E18", "#D9FFF5", "#B9F5D8", "#AAD2BA", "#6B8F71"]
tariffs = set(unelco_rates.columns)
tariffs.remove("date")
TARIFFS = sorted(list(tariffs))


fig = go.Figure()
fig.update_yaxes(title_text="kWh Produced")
for source, color in zip(SOURCES, COLORS):
    legendgroup = "non-renewable" if source == "diesel" else "renewable"
    y = []
    for date in DATES:
        data = df.query(f"source=='{source}' & date=='{date}'")
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


# TODO how to compare cost against percent of Port Vila energy not produced by renewable sources
fig2 = make_subplots(specs=[[{"secondary_y": True}]])
fig2.update_yaxes(title_text="Vatu/kWh", secondary_y=True)
fig2.update_yaxes(title_text="Vatu/Barrel", secondary_y=False)
fig2.add_trace(
    go.Bar(
        x=oil_prices["date"],
        y=oil_prices["price"],
        name="Crude Oil Price",
        marker_color=COLORS[0],
    ),
    secondary_y=False,
)
fig2.add_trace(
    go.Line(x=unelco_rates["date"], y=unelco_rates["base_rate"], name="base rate"),
    secondary_y=True,
)


#
## LAYOUT
#


# search_bar = dbc.Row(
#     [
#         # dbc.Col(dbc.Input(type="search", placeholder="Search")),
#         dbc.Col(
#             dbc.Button("Search", color="primary", className="ms-2", n_clicks=0),
#             width="auto",
#         ),
#     ],
#     className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
#     align="center",
# )

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                children=[
                                    html.Img(
                                        src="/assets/vu_flag_bg.gif",
                                        height="30px",
                                        className="mb-1",
                                    ),
                                    dbc.NavbarBrand(
                                        "Vanuatu Energy Dashboard", className="ms-2"
                                    ),
                                ],
                                className="mb-1",
                            ),
                        ],
                        align="center",
                        className="g-0",
                    ),
                ]
            ),
            # dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            # dbc.Collapse(
            #     search_bar,
            #     id="navbar-collapse",
            #     is_open=False,
            #     navbar=True,
            # ),
        ]
    ),
    color="primary",
    dark=True,
)


footer = html.Footer(
    children=[
        dbc.Row(
            [
                dbc.Col(
                    html.A(
                        "By Michael Toohig",
                        style={"color": "white"},
                        href="https://michaeltoohig.github.io",
                    ),
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.H6("Made in Vanuatu", className="text-dark"),
                            html.Img(
                                src="/assets/vu_flag_bg.gif",
                                height="20px",
                                className="ms-2 mt-1",
                            ),
                        ],
                        className="d-flex flex-row justify-content-end",
                    ),
                    className="text-end",
                ),
                # dbc.Col(
                #     html.Div(
                #         [
                #             dbc.Button("Block button", color="primary"),
                #             dbc.Button("Block button", color="secondary"),
                #         ],
                #         className="d-grid gap-2 d-md-block",
                #     )
                # ),
            ],
            className="px-5",
            justify="between",
        )
    ],
    className="bg-primary py-5 mt-5",
)


# add callback for toggling the collapse on small screens
# @app.callback(
#     Output("navbar-collapse", "is_open"),
#     [Input("navbar-toggler", "n_clicks")],
#     [State("navbar-collapse", "is_open")],
# )
# def toggle_navbar_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open


fig_controls = dbc.Card(
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


fig2_controls = dbc.Card(
    [
        html.Div(
            [
                dbc.Label("Tariff Rate"),
                dcc.Dropdown(
                    id="tariff-select",
                    options=[
                        {"value": t, "label": t.replace("_", " ")} for t in TARIFFS
                    ],
                    value="base_rate",
                    clearable=False,
                ),
            ]
        )
    ],
    body=True,
)


app.layout = html.Div(
    [
        navbar,
        dbc.Container(
            [
                html.Div(
                    [
                        html.P(DESCRIPTION),
                    ],
                    className="mt-5",
                ),
                html.Hr(),
                html.H2("Energy Sources"),
                html.P(
                    "This chart shows the amount of kilowatts/hours produced by each reported source of energy."
                ),
                # html.Hr(),
                dbc.Row([dbc.Col(fig_controls)]),
                dbc.Row(
                    [
                        dcc.Graph(id="graph", figure=fig),
                    ]
                ),
                html.H2("Port Vila's Energy Prices"),
                html.P(
                    "This chart shows the consumer kilowatt/hour price against the price of oil so the relationship between them can be compared."
                ),
                # html.Hr(),
                dbc.Row([dbc.Col(fig2_controls)]),
                dbc.Row(
                    [
                        dcc.Graph(id="graph2", figure=fig2),
                    ]
                ),
            ]
        ),
        footer,
    ]
)


@app.callback(
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


@app.callback(
    Output("graph2", "figure"),
    [
        Input("tariff-select", "value"),
    ],
)
def update_figure2_tariff(tariff):
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.update_yaxes(title_text="Tariff Rate - Vatu/kWh", secondary_y=True)
    fig2.update_yaxes(title_text="Crude Oil - Vatu/Barrel", secondary_y=False)
    fig2.add_trace(
        go.Bar(
            x=oil_prices["date"],
            y=oil_prices["price"],
            name="Crude Oil Price",
            marker_color=COLORS[3],
        ),
        secondary_y=False,
    )
    fig2.add_trace(
        go.Line(
            x=unelco_rates["date"],
            y=unelco_rates[tariff],
            name=tariff.replace("_", " "),
            marker_color=COLORS[0],
        ),
        secondary_y=True,
    )
    return fig2


if __name__ == "__main__":
    app.run_server(debug=True)
