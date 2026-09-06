from collections import defaultdict

def build_trip_routes(trips):
    trip_to_route = {}
    for trip in trips:
        trip_id = trip["trip_id"]
        route_id = trip["route_id"]
        trip_to_route[trip_id] = route_id
    return trip_to_route

def build_route_information(routes):
    route_info = {}
    for route in routes:
        route_id = route["route_id"]
        route_name = route.get("route_long_name")
        if not route_name:
            route_name = route.get("route_short_name")
        route_info[route_id] = route_name
    return route_info 

def build_stations(stops):
    stations = {}
    for stop in stops:
        stop_id = stop["stop_id"]
        stations[stop_id] = {
            "id": stop_id,
            "name": stop["stop_name"],
            "lat": float(stop["stop_lat"]),
            "lon": float(stop["stop_lon"]),
            "lines": []
        }
    return stations

def build_graphs(stop_times, trip_to_route):
    graph = defaultdict(list)
    trips = defaultdict(list)
    for item in stop_times:
        trip_id = item["trip_id"]
        stop_id = item["stop_id"]
        sequence = int(item["stop_sequence"])
        trips[trip_id].append((stop_id, sequence))

    for trip_id, stops in trips.items():
        stops.sort()
        route_id = trip_to_route.get(trip_id)
        for i in range(
            len(stops) - 1
        ):
            current_stops = stops[i][1]
            next_stop = stops[1 + 1][1]
            connection = {
                "to": next_stop,
                "route": route_id
            }

            graph[current_stops].append(connection)
    return graph

def make_graph_bidirectional(graph):
    new_graph = defaultdict(list)
    for station, connections in graph.items():
        for connection in connections:
            destination = connection["to"]
            route = connection["route"]
            new_graph[station].append({
                "to": destination,
                "route": route
            })
            new_graph[destination].append({
                "to": station,
                "route": route
            })
    return new_graph

def assign_lines_to_station(stations, graph, route_info):
    for station_id, connections in graph.items():
        for connection in connections:
            route_id = connection["route"]
            line_name = route_info.get(route_id)
            if not line_name:
                continue
            if line_name not in stations[station_id]["lines"]:
                stations[station_id]["lines"].append(line_name)
            destination = connection["to"]
            if destination in stations:
                if line_name not in stations[destination]["lines"]:
                    stations[destination]["lines"].append(line_name)
                    
    
