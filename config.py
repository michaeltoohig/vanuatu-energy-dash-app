from os import environ, path
from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"), override=True)


class Config:
    """Flask configuration variables."""

    # General Config
    # APP_NAME = environ.get("APP_NAME")
    ENV = environ.get("FLASK_ENV")
    DEBUG = environ.get("FLASK_DEBUG")
    SECRET_KEY = environ.get("SECRET_KEY")

    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATE_FOLDER = "templates"

    TITLE = "Vanuatu Energy Dashboard"
    DESCRIPTION = "An open source dashboard on Vanuatu's eneregy sources and prices from information obtained in public records."

    # chart labels and colors for URA market snapshots
    SOURCE_LABELS = ["diesel", "copra oil", "hydro", "solar", "wind"]
    SOURCE_COLORS = ["#1D1E18", "#D9FFF5", "#B9F5D8", "#AAD2BA", "#6B8F71"]
