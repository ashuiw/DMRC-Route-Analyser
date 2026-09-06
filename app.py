from flask import Flask, render_template, request, jsonify
from metro_data import metro_graph
import heapq

app = Flask(__name__)

def find_shortest_route(graph, start, end):
    if start not in graph or end not in graph:
        return None
    queue = [(0, start, [])]
    visited = set()
    while queue:
        time_taken, current_station, path = heapq.heappop(queue)
        if current_station in visited:
            continue
        visited.add(current_station)
        path = path + [current_station]
        if current_station == end:
            return {
                'path': path,
                'total_time': time_taken
            }
        for neighbor, travel_time in graph[current_station]:
            if neighbor not in visited:
                heapq.heappush(queue, (time_taken + travel_time, neighbor, path))

    return None

def calculate_interchange(route):
    interchanges = []

    interchange_stations = {
        "Rajiv Chowk",
        "Kashmere Gate",
        "Yamuna Bank",
        "Mandi House",
        "Hauz Khas",
    }

    for station in route:
        if station in interchange_stations:
            interchanges.append(station)
    return interchanges

def calculate_fare(number_of_stations):
    if number_of_stations <= 3:
        return 10
    elif number_of_stations <= 8:
        return 20
    elif number_of_stations <= 15:
        return 30
    elif number_of_stations <= 25:
        return 40

    else:
        return 50


@app.route('/')
def home():
    stations = sorted(metro_graph.keys())
    return render_template('index.html', stations=stations)

@app.route('/find-route', method=['POST'])
def find_route():
    data = request.get_json()
    start = data.get("start")
    end = data.get("end")
    if start == end:
        return jsonify({"error": "Start and end destination station cannot be same"})

    result = find_shortest_route(metro_graph, start, end)
    if not result:
        return jsonify({"error": "No route found"})
    route = result["route"]
    number_of_stations = len(route) - 1
    fare = calculate_fare(number_of_stations)
    interchanges = calculate_interchange(route)

    return jsonify({
        "start": start,
        "destination": end,
        "route": route,
        "total_stations": number_of_stations,
        "time": result["time"],
        "fare": fare,
        "interchanges": interchanges
    })

if __name__ == '__main__':
    app.run(debug=True)
    