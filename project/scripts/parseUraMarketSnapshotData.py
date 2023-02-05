import csv
import math
from datetime import datetime
from pathlib import Path
import pandas as pd


def parse_ura_source_table(df):
    date = datetime.strptime(df.columns[0], "%b-%y")
    locations = df.columns[1:]
    data = dict(date=date, locations={loc: {} for loc in locations})
    for row in df.values:
        label = row[0].lower()
        for loc, value in zip(locations, row[1:]):
            # catch empty/missing values in the table
            if value in ("-", "N/A"):
                value = "0"
            data["locations"][loc][label.lower()] = value
    return data


def main():
    data = []
    for fp in Path("data/ura-affordability-reports").glob("*-source.csv"):
        df = pd.read_csv(str(fp))
        data.append(parse_ura_source_table(df))

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


if __name__ == "__main__":
    main()
