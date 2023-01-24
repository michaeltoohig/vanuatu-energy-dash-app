from dash import register_page, html
import dash_bootstrap_components as dbc

from utils import get_latest_ura_update, get_latest_wti_update, get_latest_unelco_update


register_page(__name__, path="/about", top_nav=False)

# Unelco
latest_unelco_update = get_latest_unelco_update()

# URA
latest_ura_update = get_latest_ura_update()

# WTI
latest_wti_update = get_latest_wti_update()


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
                            We use the Utilities Regulatory Authority's electricity 
                            affordability reports for tracking the amount of electricity
                            produced by various sources across Vanuatu.
                            These reports are released each month but have been possibly
                            discontinued or just no longer available online.
                        """,
                        latest_ura_update,
                    ),
                ),
                dbc.Col(
                    data_source_card(
                        "Unelco",
                        "unelco-logo.png",
                        """
                            We use Unelco's electricity tariff reports to gather data
                            about electricity rates each month.
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
        data_sources_section
    ]
)