from flask import Flask, request, jsonify
from flask_cors import CORS
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

app = Flask(__name__)
CORS(app)

def create_data_model(depot, locations, vehicle_count, vehicle_capacity):
    data = {}
    # Locations including depot
    data['locations'] = [(depot['lat'], depot['lng'])] + [(loc['lat'], loc['lng']) for loc in locations]
    data['demands'] = [0] + [loc['demand'] for loc in locations]
    data['vehicle_capacities'] = [vehicle_capacity] * vehicle_count
    data['num_vehicles'] = vehicle_count
    data['depot'] = 0
    return data

def compute_euclidean_distance_matrix(locations):
    distances = {}
    for from_counter, from_node in enumerate(locations):
        distances[from_counter] = {}
        for to_counter, to_node in enumerate(locations):
            if from_counter == to_counter:
                distances[from_counter][to_counter] = 0
            else:
                # Euclidean distance
                distances[from_counter][to_counter] = ((from_node[0] - to_node[0])**2 + (from_node[1] - to_node[1])**2) ** 0.5
    return distances

@app.route("/optimize-vrp", methods=["POST"])
def optimize_vrp():
    try:
        data_json = request.get_json()
        depot = data_json.get("depot")
        locations = data_json.get("locations", [])
        vehicle_count = data_json.get("vehicles", 1)
        vehicle_capacity = data_json.get("capacity", 1)

        if not depot or not locations:
            return jsonify({"error": "Depot and locations are required"}), 400

        # Your optimization logic here
        # result = run_vrp_optimization(depot, locations, vehicle_count, vehicle_capacity)

        # return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Exception during optimization: {str(e)}"}), 500


    

    data = create_data_model(depot, locations, vehicle_count, vehicle_capacity)
    distance_matrix = compute_euclidean_distance_matrix(data['locations'])

    # Create routing index manager
    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    # Distance callback
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(distance_matrix[from_node][to_node] * 1000)  # scaled to integer

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Capacity constraint
    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,
        data['vehicle_capacities'],
        True,
        "Capacity"
    )

    # Setting first solution heuristic
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    # Solve
    solution = routing.SolveWithParameters(search_parameters)

    if not solution:
        return jsonify({"error": "No solution found"}), 500

    # Extract routes
    routes = []
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        route = []
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            loc = data['locations'][node_index]
            route.append({"lat": loc[0], "lng": loc[1]})
            index = solution.Value(routing.NextVar(index))
        routes.append(route)

    return jsonify({"routes": routes})

if __name__ == "__main__":
    app.run(debug=True)
