from dash import html, dcc, Input, Output, State, register_page, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

from config import SOURCE_COLORS

register_page(__name__, top_nav=True)

# -----
# Setup
# -----

unelco_rates = pd.read_csv("data/electricity.csv")
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

tariffs = set(unelco_rates.columns)
tariffs.remove("date")
TARIFFS = sorted(list(tariffs))


def build_figure_one(tariff: str = "base_rate"):
    # TODO how to compare cost against percent of Port Vila energy not produced by renewable sources
    figure = make_subplots(specs=[[{"secondary_y": True}]])
    figure.update_yaxes(title_text="Tariff Rate - Vatu/kWh", secondary_y=True)
    figure.update_yaxes(title_text="Crude Oil - Vatu/Barrel", secondary_y=False)
    figure.add_trace(
        go.Bar(
            x=oil_prices["date"],
            y=oil_prices["price"],
            name="Crude Oil Price",
            marker_color=SOURCE_COLORS[3],
        ),
        secondary_y=False,
    )
    figure.add_trace(
        go.Line(
            x=unelco_rates["date"],
            y=unelco_rates[tariff],
            name="Tariff Rate",
            marker_color=SOURCE_COLORS[0],
        ),
        secondary_y=True,
    )
    figure.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0)
    )
    return figure


def build_figure_two(tariff: str = "base_rate"):
    unelco_rates["base_rate_diff"] = unelco_rates["base_rate"].diff()
    figure = px.bar(unelco_rates, x="date", y="base_rate_diff")
    figure.update_layout(xaxis_title="Date", yaxis_title="Tariff Rate Change (Vatu)")
    figure.update_traces(marker_color=SOURCE_COLORS[0])
    return figure


figure = build_figure_one()
figure2 = build_figure_two()

# ------
# Layout
# ------

figure_controls = dbc.Card(
    [
        html.Div(
            [
                html.H6("Tariff Category Select", className="mb-0 text-white"),
                html.P("Select which tariff category is shown in the charts below.", className="small mb-1 text-white"),
                dcc.Dropdown(
                    id="tariff-select",
                    options=[
                        {"value": t, "label": t.replace("_", " ")} for t in TARIFFS
                    ],
                    value="base_rate",
                    clearable=False,
                ),
            ],
        ),
    ],
    body=True,
    color="primary",
)

notice = dbc.Alert(
    [
        html.H4("Notice", className="alert-heading"),
        html.P("Only the electricity prices for Port Vila are represented here."),
        html.Hr(),
        html.P(
            "Please get into contact with me if you have electricity prices from other provinces.",
            className="mb-0",
        ),
    ],
    color="info",
)

layout = html.Div(
    [
        html.H2("Electricity Prices"),
        notice,
        figure_controls,
        html.Div(
            [
                html.H4("Port Vila Electricity & Fuel Price"),
                html.P(
                    "This chart shows the price of electricity in Port Vila (measured in Vatu/kwh) against the price of oil (converted to Vatu/barrel) so the relationship between them can be compared."
                ),
            ],
            className="mt-3 mb-0",
        ),
        dbc.Row(
            [
                dcc.Graph(id="graph2", figure=figure),
            ],
        ),
        html.H4("Electricity Price Change Per Month"),
        html.P(
            "This chart shows the amount of change (measured in Vatu) in the electricity tariff rate compared to the month before it. Effectively showing how much the electricity price changes each month"
        ),
        dbc.Row(
            [
                dcc.Graph(id="graph3", figure=figure2),
            ]
        ),
    ]
)


@callback(
    Output("graph2", "figure"),
    Output("graph3", "figure"),
    [
        Input("tariff-select", "value"),
    ],
)
def update_figure_tariff(tariff):
    figure = build_figure_one(tariff)
    figure2 = build_figure_two(tariff)
    return figure, figure2
