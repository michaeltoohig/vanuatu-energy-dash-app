import csv
import click
import requests
from dataclasses import asdict
from pathlib import Path

from PyPDF2 import PdfFileReader

from ..unelco import extract_tariff_information, TariffInformation


@click.group("ura")
def cli():
    pass


@cli.command("fetch")
def fetch():
    """
    Fetches monthly affordability reports from http://ura.gov.vu/index.php/services/regulated-services/electricity-services/affordability
    """
    pass