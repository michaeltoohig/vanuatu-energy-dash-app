"""
This loading the data in Pandas could be improved so it isn't
repeated for each functions that perform calculations on the
dataframe.
But for now it is okay.
"""

from datetime import datetime
from typing import Tuple
import pandas as pd
from flask import current_app

# from app.config import SOURCE_LABELS


# Unelco Data
def get_unelco_data() -> pd.DataFrame:
    return pd.read_csv("app/data/electricity.csv")


def get_latest_unelco_update() -> datetime:
    unelco_data = get_unelco_data()
    return datetime.strptime(unelco_data.iloc[-1]["date"], "%Y-%m")
    # current_rate = unelco_data.iloc[-1]["base_rate"]


# URA Data
def get_ura_data() -> pd.DataFrame:
    return pd.read_csv("app/data/ura-market-snapshots.csv", thousands=",")


def get_latest_ura_update() -> datetime:
    ura_data = get_ura_data()
    return datetime.strptime(ura_data["date"].max(), "%Y-%m")


def get_latest_ura_renewable_percent() -> Tuple[float, int]:
    ura_data = get_ura_data()
    df = ura_data.loc[ura_data["date"] == ura_data["date"].max()]
    renewable = 0
    fossil = 0
    for source in current_app.config["SOURCE_LABELS"]:
        subtotal = df.loc[df["source"] == source]["kwh"].sum()
        if source == "diesel":
            fossil = subtotal
        else:
            renewable += subtotal
    total_production = renewable + fossil
    return (renewable / total_production, total_production)


# WTI Data
def get_wti_data() -> pd.DataFrame:
    return pd.read_csv("app/data/crude-oil-wti.csv")


def get_latest_wti_update() -> datetime:
    wti_data = get_wti_data()
    return datetime.strptime(wti_data["date"].max(), "%Y-%m-%d")