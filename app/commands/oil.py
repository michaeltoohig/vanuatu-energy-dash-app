"""
Fetch WTI monthly oil price averages in USD.
"""
import csv
from datetime import datetime
from io import StringIO
from pathlib import Path

import click
import requests


@click.group("oil")
def cli():
    pass


@cli.command("fetch")
def fetch():
    START_DATETIME = datetime(2019, 1, 1)  # earliest date we have local data to compare against
    URL = "https://raw.githubusercontent.com/datasets/oil-prices/master/data/wti-monthly.csv"
    resp = requests.get(URL)

    output = csv.writer(
        Path("app/data/crude-oil-wti.csv").open("w", newline=""), delimiter=",",
    )
    output.writerow(["date", "price"])

    with StringIO(resp.text) as csv_file:
        fieldnames = ["Date", "Price"]
        reader = csv.DictReader(csv_file, fieldnames=fieldnames, delimiter=",")
        next(reader)  # skip the header
        for row in reader:
            dt = datetime.strptime(row["Date"], "%Y-%m-%d")
            if dt < START_DATETIME:
                continue
            output.writerow(list(row.values()))