from datetime import datetime
import random
from dash import register_page, html, page_registry
import dash_bootstrap_components as dbc
import pandas as pd
from config import TITLE, DESCRIPTION, SOURCE_LABELS


register_page(__name__, path="/", top_nav=False)

# Unelco
unelco_rates = pd.read_csv("data/electricity.csv")
latest_unelco_update = datetime.strptime(unelco_rates.iloc[-1]["date"], "%Y-%m")
current_rate = unelco_rates.iloc[-1]["base_rate"]

# URA
df = pd.read_csv("data/ura-market-snapshots.csv", thousands=",")
latest_ura_update = datetime.strptime(df["date"].max(), "%Y-%m")

df = df.loc[df["date"] == df["date"].max()]
renewable = 0
fossil = 0
for source in SOURCE_LABELS:
    subtotal = df.loc[df["source"] == source]["kwh"].sum()
    if source == "diesel":
        fossil = subtotal
    else:
        renewable += subtotal
total_production = renewable + fossil
renewable_percent = renewable / total_production

# WTI
wti_data = pd.read_csv("data/crude-oil-wti.csv")
latest_wti_update = datetime.strptime(wti_data["date"].max(), "%Y-%m-%d")

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
        "background-image": f'linear-gradient(180deg, rgba(248,249,250,1) 50%, rgba(107,143,113,0.75) 90%), url("/assets/bg{random.randint(1,3)}.jpg")',
        "background-size": "cover",
        "background-position": "center",
    },
)


def quick_stats_card(title, description, latest_update):
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.P(title, className="card-text lead mb-0"),
                    html.H5(description, className="card-title mb-1"),
                    html.P(
                        f"Latest update {latest_update.strftime('%B %Y')}",
                        className="small my-0",
                    ),
                ],
                className="px-3 py-1",
            ),
        ],
    )


quick_stats_section = html.Div(
    [
        html.H2("Quick Stats"),
        dbc.Row(
            [
                dbc.Col(
                    quick_stats_card(
                        "Electricity Base Rate",
                        f"{current_rate} Vatu/kWh",
                        latest_unelco_update,
                    )
                ),
                dbc.Col(
                    quick_stats_card(
                        "Total Production",
                        f"{int(total_production):,} kW/h",
                        latest_ura_update,
                    )
                ),
                dbc.Col(
                    quick_stats_card(
                        "Renewable Production",
                        f"{renewable_percent:.2%}",
                        latest_ura_update,
                    )
                ),
            ]
        ),
    ],
)


def data_source_card(company, image, description, latest_update):
    return dbc.Card(
        [
            dbc.CardImg(src=f"/assets/{image}", top=True),
            dbc.CardBody(
                [
                    html.H4(company, className="card-title"),
                    html.P(description, className="small"),
                    html.P(
                        f"Latest update {latest_update.strftime('%B %Y')}",
                        className="small my-0",
                    ),
                ],
                className="px-3 py-1",
            ),
        ],
        style={
            "max-width": "400px",
        },
        className="mx-auto",
    )


data_sources_section = html.Div(
    [
        html.H2("Data Sources", className=""),
        html.P("Our sources are all publicly available reports which we parse and organize into useful formats for displaying on this website. But some of the data sources are inconsistent with their reporting schedules so our app may contain old data for that reason. All of the original source material is available on our Github page."),
        dbc.Button("View Raw Data", href="https://github.com/michaeltoohig/vanuatu-energy-dash-app/tree/master/data", outline=True, color="primary", size="lg", className="my-0 mb-3"),
        dbc.Row(
            [
                dbc.Col(
                    data_source_card(
                        "URA",
                        "ura-logo.png",
                        """
                            We use the Utilities Regulatory Authority's electricity affordability reports for tracking the amount of electricity produced by sources around Vanuatu.
                            Historically these reports were released each month.
                        """,
                        latest_ura_update,
                    ),
                ),
                dbc.Col(
                    data_source_card(
                        "Unelco",
                        "unelco-logo.png",
                        """
                            We use Unelco's electricity tariff reports to gather data about electricity rates each month.
                            Although this is only for the Port Vila area.
                            These reports are released each month usually with a one or two week delay.
                        """,
                        latest_unelco_update,
                    ),
                ),
                dbc.Col(
                    data_source_card(
                        "Oil Prices",
                        "oil-logo.png",
                        """
                            We use the WTI oil spot prices each month as a substitute for local oil prices as we have not been able to collect that data ourselves yet.
                            We convert the prices from USD to Vatu by their respective date.
                            These values are available with a one month delay.
                        """,
                        latest_wti_update,
                    ),
                ),
            ]
        ),
    ],
    # style={
    #     "padding-top": "4em",
    #     "padding-bottom": "4em",
    #     # "background": "rgb(220,227,91)",
    #     # "background": "linear-gradient(180deg, rgba(220,227,91,1) 4%, rgba(107,143,113,1) 71%, rgba(81,134,112,1) 100%)",
    # },
)


layout = html.Div(
    [
        hero,
        quick_stats_section,
        html.Hr(),
        data_sources_section,
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
