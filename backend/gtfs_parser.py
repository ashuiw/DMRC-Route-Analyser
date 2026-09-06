import csv
import os 

BASE_PATH = "data/raw/DMRC_GTFS"

def read_csv(filename):
    path = os.path.join(BASE_PATH, filename)
    with open(path, 'r', encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        return list(reader)

def load_stops():
    return read_csv(
        "stops.txt"
    )

def load_routes():
    return read_csv(
        "routes.txt"
    )

def load_trips():
    return read_csv(
        "trips.txt"
    )

def load_stop_times():
    return read_csv(
        "stop_times.txt"
    )
