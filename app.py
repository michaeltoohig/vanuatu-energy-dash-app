from dash import Dash, html, page_container, page_registry, register_page, Input, Output, State
import dash_bootstrap_components as dbc


TITLE = "Vanuatu Energy Dashboard"
DESCRIPTION = "An open source dashboard on Vanuatu's eneregy sources and prices from information obtained in public records."

app = Dash(
    __name__,
    title=TITLE,
    meta_tags=[
        {
            "name": "description",
            "content": DESCRIPTION,
        }
    ],
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

# set `server` for Heroku
server = app.server

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(
                                src="/assets/vu_flag_bg.gif",
                                height="32px",
                                className="mt-1",
                            ),
                            className="flex-grow-0"),
                        dbc.Col(
                            dbc.NavbarBrand(TITLE, className="ms-3"),
                        ),
                    ],
                    align="start",
                    className="g-0",
                ),
                href="/",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem(page["name"], href=page["path"])
                        for page in page_registry.values()
                        if page["top_nav"] == True
                    ],
                    label="Pages",
                ),
                id="navbar-collapse",
                is_open=False,
                navbar=True,
                className="d-flex justify-content-end"
            ),
        ]
    ),
    color="primary",
    dark=True,
)


# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


footer = html.Footer(
    children=[
        dbc.Row(
            [
                dbc.Col(
                    html.A(
                        "Made by Michael Toohig",
                        style={"color": "white", "text-decoration": "underline"},
                        href="https://michaeltoohig.github.io",
                    ),
                ),
                dbc.Col(
                    html.Div(
                        # [
                        #     html.H6("Made in Vanuatu", className="text-dark"),
                        #     html.Img(
                        #         src="/assets/vu_flag_bg.gif",
                        #         height="20px",
                        #         className="ms-2 mt-1",
                        #     ),
                        # ],
                        # className="text-end d-flex flex-row justify-content-end",
                    ),
                ),
            ],
            className="mx-1 mx-md-5",
            justify="around",
        )
    ],
    className="bg-primary py-5 mt-5",
)

app.layout = dbc.Container(
    [
        navbar,
        dbc.Container(children=[page_container], fluid=False, className="mt-3"),
        footer,
    ],
    fluid=True,
    className="px-0",
)

if __name__ == "__main__":
    app.run_server(debug=True)
