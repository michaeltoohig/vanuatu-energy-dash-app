from datetime import datetime
from dash import register_page, html, page_registry
import dash_bootstrap_components as dbc
import pandas as pd
from config import TITLE, DESCRIPTION


register_page(__name__, path="/", top_nav=False)

unelco_rates = pd.read_csv("data/electricity.csv")
current_rate = unelco_rates.iloc[-1]["base_rate"]
latest_update = datetime.strptime(unelco_rates.iloc[-1]["date"], "%Y-%m")

# TODO config file
df = pd.read_csv("data/ura-market-snapshots.csv", thousands=",")
df = df.loc[df["date"] == df["date"].max()]
renewable = 0
fossil = 0
SOURCES = ["diesel", "copra oil", "hydro", "solar", "wind"]
for source in SOURCES:
    subtotal = df.loc[df["source"] == source]["kwh"].sum()
    if source == "diesel":
        fossil = subtotal
    else:
        renewable += subtotal
total_production = renewable + fossil
renewable_percent = renewable / total_production

hero = html.Div(
    dbc.Container(
        [
            html.H1(TITLE, className="display-3"),
            html.P(
                DESCRIPTION,
                className="lead",
            ),
            html.Hr(className="my-2"),
            html.P("Explore the following pages."),
            html.Div(
                [
                    dbc.Button(
                        page["name"].title(),
                        color="primary",
                        size="lg",
                        href=page["path"],
                        className="me-2",
                    )
                    for page in page_registry.values()
                    if page["top_nav"] == True
                ],
                className="lead",
            ),
        ],
        fluid=True,
        className="py-3",
    ),
    className="p-3 mb-3 bg-light rounded-3",
    style={
        "background-image": 'linear-gradient(180deg, rgba(248,249,250,1) 50%, rgba(107,143,113,0.75) 90%), url("https://picsum.photos/400")',
        "background-size": "cover",
    },
)


def info_card(title, description):
    card = dbc.Card(
        [
            dbc.CardBody(
                [
                    html.P(title, className="card-text lead mb-0"),
                    html.H5(description, className="card-title mb-1"),
                ],
                className="px-3 py-1",
            ),
        ],
    )
    return card


layout = html.Div(
    [
        hero,
        html.H2("Quick Stats"),
        html.P(
            f"For the month of {latest_update.strftime('%B %Y')}",
            className="small my-0",
        ),
        dbc.Row(
            [
                dbc.Col(info_card("Electricity Base Rate", f"{current_rate} Vatu/kWh")),
                dbc.Col(
                    info_card("Total Production", f"{int(total_production):,} kW/h")
                ),
                dbc.Col(info_card("Renewable Production", f"{renewable_percent:.2%}")),
            ]
        ),
        # html.H2("Upcoming Service Disruptions"),
        # TODO
        #
        # html.H2("Data Sources"),
        # dbc.Row(
        #     [
        #         dbc.Col(info_card("Unelco Tariff Report", "September 2022")),
        #         dbc.Col(info_card("URA Affordability Report", "March 2022")),
        #         dbc.Col(info_card("WTI Oil Prices", "September 2022")),
        #     ]
        # ),
    ],
)
