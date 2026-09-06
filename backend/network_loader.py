import json

NETWORK_PATH = ("data/processed/network.json")
def load_network():
    with open(NETWORK_PATH, "r", encoding="utf-8") as file:
        return json.load(file)
    