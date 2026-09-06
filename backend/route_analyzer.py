def find_interchanges(route, stations):
    interchanges = []
    for station_id in route:
        station = stations.get(station_id)
        if not station:
            continue
        lines = station.get("lines", [])
        if len(lines) > 1:
            interchanges.append({
                "station": station["name"],
                "lines": lines
            })
    return interchanges
