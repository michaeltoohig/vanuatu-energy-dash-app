from dash import html, dcc, Input, Output, State, register_page, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


register_page(__name__, top_nav=True)

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

# TODO make config file to store common data such as these COLORS values
COLORS = ["#1D1E18", "#D9FFF5", "#B9F5D8", "#AAD2BA", "#6B8F71"]
tariffs = set(unelco_rates.columns)
tariffs.remove("date")
TARIFFS = sorted(list(tariffs))


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


unelco_rates["base_rate_diff"] = unelco_rates["base_rate"].diff()
fig3 = px.bar(unelco_rates, x="date", y="base_rate_diff", title="Base Rate Change By Month")
fig3.update_layout(xaxis_title="Date", yaxis_title="Rate Change (Vatu)")


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


layout = html.Div([
    html.H2("Port Vila's Energy Prices"),
    html.P(
        "This chart shows the consumer kilowatt/hour price against the price of oil so the relationship between them can be compared."
    ),
    dbc.Row([dbc.Col(fig2_controls)]),
    dbc.Row(
        [
            dcc.Graph(id="graph2", figure=fig2),
        ]
    ),
    html.P(
        "This chart shows the electricity price change compared to the month before."
    ),
    dbc.Row(
        [
            dcc.Graph(id="graph3", figure=fig3),
        ]
    ),
])


@callback(
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



@callback(
    Output("graph3", "figure"),
    [
        Input("tariff-select", "value"),
    ],
)
def update_figure2_tariff(tariff):
    unelco_rates["diff"] = unelco_rates[tariff].diff()
    figure = px.bar(unelco_rates, x="date", y="diff", labels=["tariff"])
    figure.update_layout(yaxis_title=f"{tariff.replace('_', ' ').title()} Change (Vatu)")
    return figure

