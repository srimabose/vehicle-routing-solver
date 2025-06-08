import numpy as np
from scipy.spatial import distance_matrix
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpBinary, PULP_CBC_CMD
import time
import matplotlib.pyplot as plt

# Node coordinates
coords_raw = [
    [82,76],[96,44],[50,5],[49,8],[13,7],[29,89],[58,30],[84,39],
    [14,24],[2,39],[3,82],[5,10],[98,52],[84,25],[61,59],[1,65],
    [88,51],[91,2],[19,32],[93,3],[50,93],[98,14],[5,42],[42,9],
    [61,62],[9,97],[80,55],[57,69],[23,15],[20,70],[85,60],[98,5]
]
coords = np.array(coords_raw)

# Demands for each node
demands = [0, 19, 21, 6, 19, 7, 12, 16, 6, 16, 8, 14, 21, 16, 3, 22, 18, 19,
           1, 24, 8, 12, 4, 8, 24, 24, 2, 20, 15, 2, 14, 9]

vehicle_capacity = 100
num_nodes = len(coords)
dist_mat = distance_matrix(coords, coords)

# Solver wrapper
def solve_cvrp(nodes_idx, demands_sub, dist_sub, vehicle_capacity, allowed_edges=None):
    n = len(nodes_idx)
    prob = LpProblem("CVRP", LpMinimize)

    # Variables
    x = {}
    for i in range(n):
        for j in range(n):
            if i != j:
                if allowed_edges is None or (nodes_idx[i], nodes_idx[j]) in allowed_edges:
                    x[(i, j)] = LpVariable(f"x_{i}_{j}", cat=LpBinary)
                else:
                    x[(i, j)] = 0
            else:
                x[(i, j)] = 0

    u = {i: LpVariable(f"u_{i}", lowBound=demands_sub[i], upBound=vehicle_capacity)
         for i in range(1, n)}

    # Objective
    prob += lpSum(dist_sub[i][j] * x[(i, j)] for i in range(n) for j in range(n)
                  if i != j and x[(i, j)] != 0)

    # Constraints
    for j in range(1, n):
        prob += lpSum(x[(i, j)] for i in range(n) if i != j and x[(i, j)] != 0) == 1
        prob += lpSum(x[(j, i)] for i in range(n) if i != j and x[(j, i)] != 0) == 1

    prob += lpSum(x[(0, j)] for j in range(1, n) if x[(0, j)] != 0) <= vehicle_capacity
    prob += lpSum(x[(i, 0)] for i in range(1, n) if x[(i, 0)] != 0) == lpSum(
        x[(0, j)] for j in range(1, n) if x[(0, j)] != 0)

    for i in range(1, n):
        for j in range(1, n):
            if i != j and x[(i, j)] != 0:
                prob += u[i] - u[j] + vehicle_capacity * x[(i, j)] <= vehicle_capacity - demands_sub[j]

    # Solve with time limit and verbosity
    solver = PULP_CBC_CMD(msg=1, timeLimit=30)
    print(f"Solving CVRP with {n} nodes...")
    prob.solve(solver)
    print("Solving complete.")

    return prob.objective.value()

# For faster testing, reduce to 10 nodes (0 to 9)
test_node_count = 10
full_nodes = list(range(test_node_count))
coords = coords[:test_node_count]
dist_mat = distance_matrix(coords, coords)
demands = demands[:test_node_count]

# --- 1. Pure Branch-and-Cut ---
start = time.time()
total_dist_full = solve_cvrp(full_nodes, demands, dist_mat, vehicle_capacity)
time_full = time.time() - start

# --- 2. KMeans Clustering ---
num_clusters = 2
kmeans = KMeans(n_clusters=num_clusters, random_state=0)
clusters = kmeans.fit_predict(coords[1:])  # exclude depot
clusters = np.insert(clusters, 0, -1)      # depot in cluster -1

total_dist_kmeans = 0
start = time.time()
for cluster_id in range(num_clusters):
    cluster_nodes_idx = [0] + [i for i in range(1, test_node_count) if clusters[i] == cluster_id]
    sub_coords = coords[cluster_nodes_idx]
    sub_demands = [demands[i] for i in cluster_nodes_idx]
    sub_dist = distance_matrix(sub_coords, sub_coords)
    dist = solve_cvrp(cluster_nodes_idx, sub_demands, sub_dist, vehicle_capacity)
    total_dist_kmeans += dist
time_kmeans = time.time() - start

# --- 3. Hybrid KNN + Branch-and-Cut ---
k = 3
nbrs = NearestNeighbors(n_neighbors=k+1).fit(coords)
_, knn_indices = nbrs.kneighbors(coords)

allowed_edges_hybrid = set()
for i in range(test_node_count):
    for j in knn_indices[i][1:]:
        allowed_edges_hybrid.add((i, j))
        allowed_edges_hybrid.add((j, i))

start = time.time()
total_dist_hybrid = solve_cvrp(full_nodes, demands, dist_mat, vehicle_capacity, allowed_edges_hybrid)
time_hybrid = time.time() - start

# --- Results ---
print("\nMethod                          | Total Distance")
print("--------------------------------|----------------------")
print(f"1) Only Branch-and-Cut           | {total_dist_full:.2f}")
print(f"2) KMeans + Branch-and-Cut       | {total_dist_kmeans:.2f}")
print(f"3) Hybrid KNN + Branch-and-Cut   | {total_dist_hybrid:.2f}")

# --- Plot ---
methods = ['Pure Branch-and-Cut', 'KMeans + Branch-and-Cut', 'Hybrid KNN + Branch-and-Cut']
distances = [total_dist_full, total_dist_kmeans, total_dist_hybrid]

plt.figure(figsize=(8, 6))
bars = plt.bar(methods, distances, color=['skyblue', 'salmon', 'limegreen'])
plt.title('Total Distance Comparison')
plt.ylabel('Total Distance')
plt.ylim(0, max(distances) * 1.2)

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval:.2f}', ha='center', fontsize=11)

plt.tight_layout()
plt.show()
