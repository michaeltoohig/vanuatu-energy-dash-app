import csv
import click
import requests
from dataclasses import asdict
from pathlib import Path

from PyPDF2 import PdfFileReader

from ..unelco import extract_tariff_information, TariffInformation


@click.group("unelco")
def cli():
    pass


@cli.command("fetch")
def fetch():
    """
    Fetch Unelco's latest electricity tariff report.
    Unelco will also provide via email upon request (not any longer).
    """
    URL = "https://www.unelco.engie.com/images/doc/electricityrate.pdf"
    resp = requests.get(URL)
    resp.raise_for_status()
    Path("app/data/unelco-tariff-reports/downloaded.pdf").write_bytes(resp.content)
    click.echo("Check download.pdf and rename YYYY-MM.pdf")


@cli.command("extract")
def extract():
    reports = []
    # extract information from pdf
    for path in Path("app/data/unelco-tariff-reports").glob("*.pdf"):
        print(f"Opening {path.name}")
        with path.open("rb") as f:
            pdf = PdfFileReader(f)
            page = pdf.getPage(0)
            lines = page.extractText().split("\n")
        try:
            data = extract_tariff_information(lines)
        except ValueError:
            print(f"-- Failed {path.name}")
        reports.append(
            TariffInformation(
                date=path.stem.strip(),
                **data,
            )
        )
    # extract information from csv
    for path in Path("app/data/unelco-tariff-reports").glob("*.csv"):
        print(f"Opening {path.name}")
        with path.open("r") as f:
            reader = csv.DictReader(f)
            data = {k: float(v) for k, v in next(reader).items()}
        reports.append(
            TariffInformation(
                date=path.stem.strip(),
                **data,
            )
        )
    # save combined results
    with open("app/data/electricity.csv", "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(asdict(reports[0]).keys()))
        writer.writeheader()
        for report in sorted(reports, key=lambda i: i.date):
            writer.writerow(asdict(report))
