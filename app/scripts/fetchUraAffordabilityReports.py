"""
Fetches monthly affordability reports from http://ura.gov.vu/index.php/services/regulated-services/electricity-services/affordability
"""

from datetime import datetime
from pathlib import Path
import shutil

import requests
from bs4 import BeautifulSoup

URA_BASE_URL = "http://ura.gov.vu"
resp = requests.get(
    f"{URA_BASE_URL}/index.php/services/regulated-services/electricity-services/affordability"
)
resp.raise_for_status()
html = resp.text
soup = BeautifulSoup(html, "html.parser")


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


save_path = Path("data/ura-affordability-reports")
for uri, date in downloads:
    report_file = save_path / datetime.strftime(date, "%Y-%m.pdf")
    # https://stackoverflow.com/a/39217788
    with requests.get(f"{URA_BASE_URL}{uri}", stream=True) as r:
        with report_file.open("wb") as f:
            shutil.copyfileobj(r.raw, f)
