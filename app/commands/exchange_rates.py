import csv
import shutil
from datetime import datetime
from pathlib import Path

import click
import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://www.exchangerates.org.uk"


@click.group("exchange_rates")
def cli():
    pass


@cli.command("fetch")
def fetch():
    for year in ["2023"]:  #["2017", "2018", "2019", "2020", "2021", "2022"]:
        resp = requests.get(f"{BASE_URL}/VUV-USD-spot-exchange-rates-history-{year}.html")
        resp.raise_for_status()
        html = resp.text
        # soup = BeautifulSoup(html, "html.parser")
        with open(
            f"app/data/exchange-rates/vuv-usd-spot-exchange-rates-{year}.html", "w"
        ) as file:
            file.write(html)

    daily = csv.writer(
        Path("app/data/exchange-rates/daily.csv").open("w", newline=""), delimiter=","
    )
    daily.writerow(["date", "exchange_rate"])
    monthly_file = Path("app/data/exchange-rates/monthly.csv")
    monthly = csv.writer(
        monthly_file.open("w", newline=""), delimiter=","
    )
    monthly.writerow(["date", "exchange_rate"])

    for file in sorted(Path("app/data/exchange-rates").glob("*.html")):
        soup = BeautifulSoup(file.open("r").read(), "html.parser")
        for h3 in soup.find("div", {"id": "hd-maintable"}).find_all("h3"):
            date = datetime.strptime(h3.text, "%B %Y")
            table = h3.find_next_sibling("table")
            dailyrows = table.find_all("tr")[1:-1]
            for row in dailyrows:
                dt = datetime.strptime(row.td.text.split(" ", 1)[1].strip(), "%d %B %Y")
                rate = float(row.find_all("td")[1].text.split("$")[1])
                daily.writerow([dt.strftime("%Y-%m-%d"), rate])
            monthlyrow = table.find_all("tr")[-1]
            average = float(monthlyrow.td.text.rsplit(":", 1)[-1].strip())
            monthly.writerow([date.strftime("%Y-%m"), average])

    daily.close()
    monthly.close()

    # copy monthly data to app - later we should process the exchange rate info in place with the electricity price data rather than doing that work in the app
    # tmp_file_for_app = Path("app/data/exchange-rates.csv")
    # shutil.copy(monthly_file, tmp_file_for_app)

