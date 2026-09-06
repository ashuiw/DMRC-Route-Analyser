from flask import (Flask, render_template, request, jsonify)

from backend.network_loader import load_network
from backend.route_finder import find_shortest_route
from backend.route_analyzer import analyze_route
from backend.fare_calculator import calculate_fare

app = Flask(__name__)

network = load_network()

stations = network["stations"]
graph = network["graph"]
routes = network["routes"]

@app.route("/")
def home():
    station_list = []
    for station_id, station in stations.items():
        station_list.append({
            "id": station_id,
            "name": station["name"]
        })
    station_list.sort(key=lambda x: x["name"])
    return render_template("index.html", stations=station_list)

@app.route("/api/route", methods=["POST"])
def get_route():
    data = request.get_json()
    start = data.get("start")
    destination = data.get("destination")

    if not start or not destination:
        return jsonify({"error": "Both start and destination stations are required."}), 400

    result = find_shortest_route(graph, start, destination)

    if not result:
        return jsonify({"error": "No route found between the specified stations."}), 404

    route = result["route"]

    analysis = analyze_route(route, graph, stations, routes)
    total_stations = (len(route) - 1)
    fare = calculate_fare(total_stations)


    return jsonify({
        "success": True,
        "route": analysis["stations"],
        "total_stations": total_stations,
        "interchanges": analysis["interchanges"],
        "fare": fare,
        "fare_status": "Fare calculated based on the number of stations traveled."
    })

if __name__ == "__main__":
    app.run(debug=True)