"""
Fetches monthly exchange rate from https://www.exchangerates.org.uk/VUV-USD-spot-exchange-rates-history-20xx.html
"""
import csv
from datetime import datetime
from pathlib import Path
import shutil

import requests
from bs4 import BeautifulSoup

# BASE_URL = "https://www.exchangerates.org.uk"

# for year in ["2017", "2018", "2019", "2020", "2021", "2022"]:
#     resp = requests.get(f"{BASE_URL}/VUV-USD-spot-exchange-rates-history-{year}.html")
#     resp.raise_for_status()
#     html = resp.text
#     # soup = BeautifulSoup(html, "html.parser")
#     with open(
#         f"data/exchange-rates/vuv-usd-spot-exchange-rates-{year}.html", "w"
#     ) as file:
#         file.write(html)

daily = csv.writer(
    Path("data/exchange-rates/daily.csv").open("w", newline=""), delimiter=","
)
monthly = csv.writer(
    Path("data/exchange-rates/monthly.csv").open("w", newline=""), delimiter=","
)

for file in sorted(Path("data/exchange-rates").glob("*.html")):
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
