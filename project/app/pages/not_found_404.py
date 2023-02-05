from dash import html
import dash
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/404", top_nav=False)


layout = html.Div(
    dbc.Container(
        [
            html.H1("404 Not Found"),
            dbc.Button("Go Home", size="lg", color="primary", href="/"),
        ],
        className="py-3 text-center",
    )
)
