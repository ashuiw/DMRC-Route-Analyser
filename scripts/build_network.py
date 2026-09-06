import json 
import os

from backend.gtfs_parser import (
    load_stops,
    load_routes,
    load_trips,
    load_stop_times
)

from backend.graph_builder import (
    build_trip_routes,
    build_route_information,
    build_stations,
    build_graphs,
    make_graph_bidirectional,
    assign_lines_to_station
)

def main():
    print("Building Network...")
    stops = load_stops()
    routes = load_routes()
    trips = load_trips()
    stop_times = load_stop_times()

    trip_to_route = build_trip_routes(trips)
    route_info = build_route_information(routes)
    stations = build_stations(stops)
    graph = build_graphs(stop_times, trip_to_route)
    graph = make_graph_bidirectional(graph)
    assign_lines_to_station(stations, graph, route_info)

    network = {
        "stations": stations,
        "graph": graph,
        "routes": route_info
    }

    os.makedirs("data/processed", exist_ok=True)
    with open("data/processed/network.json", "w", encoding="utf-8") as file:
        json.dump(network, file, indent=2)
    print("Network Built Successfully!")

if __name__ == "__main__":
    main()