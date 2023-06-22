import random
from flask import current_app as app
from flask import render_template, url_for
import markdown
import markdown.extensions.fenced_code
from pygments.formatters.html import HtmlFormatter
from markupsafe import Markup

from .utils import get_unelco_data, get_latest_unelco_update, get_latest_ura_update, get_latest_ura_renewable_percent, get_latest_wti_update


@app.route("/")
def index():
    # Unelco
    unelco_data = get_unelco_data()
    latest_unelco_update = get_latest_unelco_update()
    current_rate = unelco_data.iloc[-1]["base_rate"]

    # URA
    latest_ura_update = get_latest_ura_update()
    renewable_percent, total_production = get_latest_ura_renewable_percent()

    hero_image = url_for("static", filename=f"bg{random.randint(1, 3)}.jpg")

    return render_template(
        "index.html",
        content="",
        styles="",
        hero_image=hero_image,
        current_rate=f"{current_rate} Vatu/kWh",
        latest_unelco_update=latest_unelco_update.strftime("%B %Y"),
        total_production=f"{int(total_production)} kWh",
        renewable_percent=f"{renewable_percent:.2%}",
        latest_ura_update=latest_ura_update.strftime("%B %Y"),
    )

@app.route("/about")
def about():
    latest_unelco_update = get_latest_unelco_update()
    latest_ura_update = get_latest_ura_update()
    latest_wti_update = get_latest_wti_update()
    sources = [
        dict(
            title="URA",
            description="We use the Utilities Regulatory Authority's electricity affordability reports for tracking the amount of electricity produced by various sources across Vanuatu. These reports are released each month but have been possibly discontinued or just no longer available online.",
            latest_update=latest_ura_update,
            image=url_for("static", filename="ura-logo.png"),
        ),
        dict(
            title="Uneclo",
            description="We use Unelco's electricity tariff reports to gather data about electricity rates each month. Although this is only for the Port Vila area. These reports are released each month usually with a one or two week delay.",
            latest_update=latest_unelco_update,
            image=url_for("static", filename="unelco-logo.png"),
        ),
        dict(
            title="Oil Prices",
            description="We use the WTI oil spot prices each month as a substitute for local oil prices as we have not been able to collect that data ourselves yet. We convert the prices from USD to Vatu by their respective date. These values are available with a one month delay.",
            latest_update=latest_wti_update,
            image=url_for("static", filename="oil-logo.png"),
        ),
    ]
    return render_template(
        "about.html",
        sources=sources,
    )

# @app.route("/")
# def index():
#     with open("README.md", "r") as fp:
#         formatter = HtmlFormatter(
#             style="solarized-light", full=True, cssclass="codehilite",
#         )
#         styles = f"<style>{formatter.get_style_defs()}</style>"
#         html = (
#             markdown.markdown(fp.read(), extensions=["codehilite", "fenced_code"])
#             .replace(
#                 # Fix relative path for image(s) when rendering README.md on index page
#                 'src="app/',
#                 'src="',
#             )
#             .replace("codehilite", "codehilite p-2 mb-3")
#         )
#         return render_template(
#             "index.html", content=Markup(html), styles=Markup(styles),
#         )