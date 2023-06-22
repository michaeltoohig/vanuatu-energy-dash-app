import csv
import shutil
from datetime import datetime
from pathlib import Path

import click
import requests
from bs4 import BeautifulSoup
import pandas as pd

from ..ura import extract_source_figure, extract_source_table, parse_source_table


@click.group("ura")
def cli():
    pass


@cli.command("fetch")
def fetch():
    """
    Fetches monthly affordability reports from http://ura.gov.vu/index.php/services/regulated-services/electricity-services/affordability
    """
    BASE_URL = "http://ura.gov.vu"
    resp = requests.get(f"{BASE_URL}/index.php/services/regulated-services/electricity-services/affordability")
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # extract each pdf download link from the page
    downloads = []
    for p_tag in soup.find_all("p"):
        if "energy market report" not in p_tag.text.lower():
            continue
        year = datetime.strptime(p_tag.text.strip()[-4:], "%Y")
        reports = p_tag.find_next_sibling("table").find_all("a")
        for report_tag in reports:
            name = report_tag.text.strip()
            if name == "":
                continue  # edge case
            month = datetime.strptime(name.split()[0], "%B")
            date = datetime(year.year, month.month, day=1)
            url = report_tag.attrs.get("href")
            downloads.append((url, date))

    # Save each report to local directory
    save_path = Path("app/data/ura-affordability-reports")
    for uri, date in downloads:
        report_file = save_path / datetime.strftime(date, "%Y-%m.pdf")
        # https://stackoverflow.com/a/39217788
        with requests.get(f"{BASE_URL}{uri}", stream=True) as r:
            with report_file.open("wb") as f:
                shutil.copyfileobj(r.raw, f)


@cli.command("extract-data")
def extract_data():
    for path in Path("app/data/ura-affordability-reports").glob("*.pdf"):
        print(f"Opening {path.name}")
        extract_source_figure(path)
        extract_source_table(path)


@cli.command("parse")
def parse():
    data = []
    for fp in Path("data/ura-affordability-reports").glob("*-source.csv"):
        df = pd.read_csv(str(fp))
        data.append(parse_source_table(df))

    fieldnames = [
        "date",
        "location",
        "source",
        "kwh",
    ]
    with open("app/ura-market-snapshots.csv", "w") as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writeheader()
        for d in data:
            date = d["date"]
            for location in d["locations"].keys():
                try:
                    kwh_str = d["locations"][location]["total kwh produced"]
                    total_kwh_produced = int(kwh_str.replace(",", ""))
                except TypeError:
                    total_kwh_produced = None
                for source in filter(
                    lambda field: "%" in field, d["locations"][location].keys()
                ):
                    if total_kwh_produced:
                        source_percentage = d["locations"][location][source]
                        kwh_produced_percent = float(source_percentage.strip("%")) / 100
                        kwh = kwh_produced_percent * total_kwh_produced
                    else:
                        kwh = None
                    row = dict(
                        date=date.strftime("%Y-%m"),
                        location=location.strip().replace("\n", "").replace("*", ""),
                        source=source.replace("%", "").strip(),
                        kwh=kwh,
                    )
                    csvwriter.writerow(row)
