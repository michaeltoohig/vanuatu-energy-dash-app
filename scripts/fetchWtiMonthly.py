"""
Fetch WTI monthly oil price averages in USD.
"""
# TODO

import requests

URL = "https://raw.githubusercontent.com/datasets/oil-prices/master/data/wti-monthly.csv"

resp = requests.get(URL)