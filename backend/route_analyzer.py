def analyze_route(route, graph, stations, route_info):
    route_details = []
    current_line = None
    interchanges = []
    for i in range(len(route)):
        station_id = route[i]
        station = station[station_id]
        line = None
        if i < len(route) - 1:
            next_station = route[i + 1]
            connections = graph.get(station_id, [])
            for connection in connections:
                if connection["to"] == next_station:
                    route_id = connection["route"]
                    line = route_info.get(route_id)
                    break
                route_details.append({
                    "station": station["name"],
                    "line": line
                })
                if (current_line and line and current_line != line):
                    interchanges.append({
                        "station": station['name'],
                        "from": current_line,
                        "to": line
                    })
                if line:
                    current_line = line
    return{
        "stations": route_details,
        "interchanges": interchanges
    }