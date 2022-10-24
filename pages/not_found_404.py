from dash import html
import dash

dash.register_page(__name__, path="/404", top_nav=False)


layout = html.H1("Custom 404")