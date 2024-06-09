"""Simple InfluxDB Bucket Exporter

This script will export all data from a bucket in a specific time range to CSV.
    """
import csv
from datetime import datetime
from influxdb_client import InfluxDBClient

# Configuration

URL = ""  # INSERT your InfluxDB URL
ORGANISATION = ""  # INSERT your InfluxDB organisation
BUCKET = ""  # INSERT your InfluxDB bucket
TOKEN = ""  # INSERT your InfluxDB API token
RANGE_START = "2023-01-01T00:00:00Z"  # REPLACE with your custom time range start ...
# RANGE_END = "2023-12-31T23:59:59Z" # ... and end or comment this line out and the following in to use the current time as endtime
RANGE_END = datetime.now().strftime(r"%Y-%m-%dT%H:%M:%SZ")
RANGE_END_DATE = datetime.strptime(RANGE_END, r"%Y-%m-%dT%H:%M:%SZ").strftime(
    "%Y-%m-%d"
)


with InfluxDBClient(url=URL, token=TOKEN, org=ORGANISATION) as client:

    csv_iterator = client.query_api().query_csv(
        'from(bucket:"'
        + BUCKET
        + '") |> range(start: '
        + RANGE_START
        + ", stop: "
        + RANGE_END
        + ")"
    )

    output = csv_iterator.to_values()


with open(
    RANGE_END_DATE + "_export_" + BUCKET + ".csv",
    mode="w",
    newline="",
    encoding="utf-8",
) as file:
    writer = csv.writer(file)
    writer.writerows(output)
