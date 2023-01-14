from datetime import datetime
import random
from dash import register_page, html, page_registry
import dash_bootstrap_components as dbc
import pandas as pd
from config import TITLE, DESCRIPTION, SOURCE_LABELS
from utils import get_latest_ura_update, get_latest_wti_update, get_unelco_data, get_latest_unelco_update, get_latest_ura_renewable_percent


register_page(__name__, path="/", top_nav=False)

# Unelco
unelco_data = get_unelco_data()
latest_unelco_update = get_latest_unelco_update()
current_rate = unelco_data.iloc[-1]["base_rate"]

# URA
latest_ura_update = get_latest_ura_update()
renewable_percent, total_production = get_latest_ura_renewable_percent()

# WTI
latest_wti_update = get_latest_wti_update()

hero = html.Div(
    dbc.Container(
        [
            html.H1(TITLE, className="display-3"),
            html.P(
                DESCRIPTION,
                className="lead",
            ),
            html.Hr(className="my-2"),
            html.P("All sources come from public information."),
            dbc.Button(
                "Learn More",
                color="primary",
                href="/about",
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

layout = html.Div(
    [
        hero,
        quick_stats_section,
        html.Hr(),
        html.H2("Explore our pages"),
        html.Div(
            [
                dbc.Button(
                    page["name"].title(),
                    color="primary",
                    outline=True,
                    size="lg",
                    href=page["path"],
                    className="me-2",
                )
                for page in page_registry.values()
                if page["top_nav"] == True
            ],
            className="lead",
        ),
        # html.Hr(),
        # data_sources_section,
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
