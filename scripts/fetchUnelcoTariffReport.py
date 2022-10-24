"""
Fetch Unelco's latest electricity tariff report.
Unelco will also provide via email upon request.
"""
# TODO

from datetime import datetime
import requests

# URL of current month electricity tariff rate
URL = "https://www.unelco.engie.com/images/doc/electricityrate.pdf"

resp = requests.get(URL)