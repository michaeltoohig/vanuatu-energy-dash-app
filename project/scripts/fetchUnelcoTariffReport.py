"""
Fetch Unelco's latest electricity tariff report.
Unelco will also provide via email upon request (not any longer).
"""
from pathlib import Path
import requests

URL = "https://www.unelco.engie.com/images/doc/electricityrate.pdf"
resp = requests.get(URL)
resp.raise_for_status()
output = Path("data/unelco-tariff-reports/downloaded.pdf").write_bytes(resp.content)

# User must check file is new and give YYYY-MM.pdf filename.
print("Check downloaded.pdf and rename YYYY-MM.pdf")