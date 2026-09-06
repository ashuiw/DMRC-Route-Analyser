import heapq

def find_shortest_route(graph, start, destination):
    queue = []
    heapq.heappush(queue, (0, start, [start]))
    visited = set()
    while queue:
        cost, station, path = heapq.heappop(queue)
        if station in visited:
            continue
        visited.add(station)
        path = path + [station]
        if station == destination:
            return {"route": path, "cost": cost}
        for connection in graph.get(station, []):
            next_station = connection["to"]
            if next_station not in visited:
                heapq.heappush(queue, (cost + 1, next_station, path))

    return None