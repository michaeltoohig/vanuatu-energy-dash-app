from dash import register_page, html
import dash_bootstrap_components as dbc

register_page(__name__, path="/", top_nav=False)

jumbotron = html.Div(
    dbc.Container(
        [
            html.H1("Open Source Energy Dashboard", className="display-3"),
            html.P(
                "Use Containers to create a jumbotron to call attention to "
                "featured content or information.",
                className="lead",
            ),
            html.Hr(className="my-2"),
            html.P(
                "Use utility classes for typography and spacing to suit the "
                "larger container."
            ),
            html.P(
                dbc.Button("Learn more", color="primary"), className="lead"
            ),
        ],
        fluid=True,
        className="py-3",
    ),
    className="p-3 bg-light rounded-3",
    # style={
    #     "background-image": 'linear-gradient(to bottom, rgba(245, 246, 252, 0.52), rgba(117, 19, 93, 0.73)), url("https://picsum.photos/400")',
    #     "background-size": "cover",
    # TODO
    # },
)


def info_card(title, description):
    card = dbc.Card([
        dbc.CardBody(
            [
                html.H4(title, className="card-title"),
                html.P(description, className="card-text"),
                # dbc.Button("Go somewhere", color="primary"),
            ]
        ),
    ])
    return card

# TODO use Markdown to write intro and about pages
layout = html.Div(
    [
        dbc.Row([
            html.P("""
                An open-source application to explore publicly available informtaion
                about the energy market in Vanuatu. Note this is an incomplete application.
            """)
        ]),
        dbc.Row([
            dbc.Col(info_card("Last Updated", "September 2022")),
            dbc.Col(info_card("Raw Data", "Find raw data we use for this project on our Github repo.")),
            dbc.Col(info_card("", "")),
        ])
    ],
)
