# 🚚 Hybrid CVRP Optimizer Web App

A web-based application that solves the **Capacitated Vehicle Routing Problem (CVRP)** using a **hybrid algorithm** combining **K-Nearest Neighbors (KNN)** for graph reduction and **Branch-and-Cut** for exact optimization. The app takes user input for coordinates, number of vehicles, and vehicle capacity, and returns optimized delivery routes with visualizations.

---

## 📌 Problem Statement

The Capacitated Vehicle Routing Problem (CVRP) is a classic combinatorial optimization problem where the goal is to determine the optimal set of routes for a fleet of vehicles to deliver goods to a set of customers. Each vehicle has a limited carrying capacity, and each customer has a fixed demand. The objective is to minimize the total distance traveled, while ensuring:
- Each customer is visited exactly once
- The total demand on each route does not exceed vehicle capacity

---

## 🚀 Features

- **User-friendly Interface** to input customer and depot coordinates
- **Custom vehicle configuration**: define number of vehicles and capacity
- **Efficient optimization** using hybrid KNN + Branch-and-Cut method
- **Interactive Visual Output**: Route plots and distance matrix heatmap
- **Scalable for medium-sized instances** like `A-n33-k5` from CVRPLIB

---

## 🧠 Approach

1. **Graph Reduction using KNN**  
   Only retain the most relevant edges in the distance matrix using KNN to reduce problem complexity.

2. **MILP Formulation on Reduced Graph**  
   Formulate the CVRP as a Mixed-Integer Linear Program using only KNN edges.

3. **Branch-and-Cut Algorithm**  
   Solve the MILP using Branch-and-Cut to iteratively eliminate subtours and converge to the optimal solution.

---

## 🛠 Technologies Used

- **Frontend**: HTML, CSS, JavaScript *(or React)*
- **Backend**: Python (Flask / FastAPI)
- **Optimization Libraries**: PuLP, Gurobi, or CPLEX
- **Machine Learning**: scikit-learn (KNN)
- **Visualization**: Matplotlib, Seaborn, NetworkX

---

## 🖥️ How to Run Locally

```bash
git clone https://github.com/your-username/hybrid-cvrp-optimizer.git
cd hybrid-cvrp-optimizer
pip install -r requirements.txt
python app.py

## 📥 Inputs Required

- **Coordinates of Warehouse (Depot):**  
  The location of the central depot in the form of (x, y) coordinates.

- **Coordinates of Customers:**  
  A list of customer locations, each represented by (x, y) coordinates. Optionally, demand per customer can be included.

- **Number of Vehicles:**  
  The total number of delivery vehicles available for routing.

- **Capacity of Each Vehicle:**  
  Maximum load each vehicle can carry. This constraint ensures no vehicle is overloaded during delivery.

---

## 📤 Outputs

- **Optimized Delivery Route per Vehicle:**  
  For each vehicle, the sequence of customer visits is provided in order, starting and ending at the depot.

- **Total Distance Traveled:**  
  The cumulative distance covered by all vehicles, which is minimized by the hybrid optimization algorithm.

- **Graph Showing Customer Paths and Depot:**  
  A plotted visual representation of all routes taken by vehicles, showing the depot and customer nodes.

- **Heatmap of Distance Matrix for Visualization:**  
  A visual heatmap showing the distances between all node pairs, useful for analyzing proximity and clustering.

---

## 📝 Dataset Used

**Benchmark CVRP Dataset:** `A-n33-k5`  
- **Number of Customers:** 33  
- **Number of Vehicles:** 5  
- **Vehicle Capacity:** 100  

This dataset is sourced from the standard Augerat dataset for benchmarking VRP algorithms.

---

## 📚 Project Background

This project is based on a research thesis titled:  
**“Optimization of Capacitated Vehicle Routing Problem using a Hybrid KNN + Branch-and-Cut Approach”**  
by **Srima Bose**  
*M.Sc. Mathematics and Scientific Computing, MNNIT Allahabad*

---

## 🙏 Acknowledgements

Special thanks to:

- **Prof. Pitam Singh** – for valuable supervision  
- **Miss Soni Yadav (PhD Scholar)** – for constant support and guidance throughout the project

---

## 🪪 License

This project is open-sourced under the **MIT License**.  
See the [LICENSE](LICENSE) file for more information.

