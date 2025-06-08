import React, { useState } from "react";
import MapView from "./MapView";

function App() {
  const [depot, setDepot] = useState({ lat: "", lng: "" });
  const [vehicles, setVehicles] = useState(1);
  const [capacity, setCapacity] = useState(1);
  const [locations, setLocations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [optimizedRoutes, setOptimizedRoutes] = useState(null);

  const handleAddLocation = (e) => {
    e.preventDefault();
    const lat = parseFloat(e.target.latitude.value);
    const lng = parseFloat(e.target.longitude.value);
    const demand = parseInt(e.target.demand.value);
    if (!isNaN(lat) && !isNaN(lng) && !isNaN(demand)) {
      setLocations([...locations, { lat, lng, demand }]);
    }
    e.target.reset();
  };

  const handleOptimize = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:5000/optimize-vrp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          depot,
          vehicles,
          capacity,
          locations,
        }),
      });
      const data = await response.json();
      setOptimizedRoutes(data.routes); // Expect routes per vehicle
    } catch (err) {
      alert("Error optimizing VRP");
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Vehicle Routing Problem Optimizer</h1>

      <div>
        <h3>Depot Location</h3>
        <input
          type="number"
          step="any"
          placeholder="Depot Latitude"
          value={depot.lat}
          onChange={(e) => setDepot({ ...depot, lat: e.target.value })}
          required
        />
        <input
          type="number"
          step="any"
          placeholder="Depot Longitude"
          value={depot.lng}
          onChange={(e) => setDepot({ ...depot, lng: e.target.value })}
          required
        />
      </div>

      <div>
        <h3>Vehicle Details</h3>
        <input
          type="number"
          min="1"
          placeholder="Number of Vehicles"
          value={vehicles}
          onChange={(e) => setVehicles(parseInt(e.target.value))}
          required
        />
        <input
          type="number"
          min="1"
          placeholder="Vehicle Capacity"
          value={capacity}
          onChange={(e) => setCapacity(parseInt(e.target.value))}
          required
        />
      </div>

      <div>
        <h3>Add Delivery Location</h3>
        <form onSubmit={handleAddLocation}>
          <input type="number" step="any" name="latitude" placeholder="Latitude" required />
          <input type="number" step="any" name="longitude" placeholder="Longitude" required />
          <input type="number" name="demand" placeholder="Demand" required />
          <button type="submit">Add Location</button>
        </form>
      </div>

      <div>
        <h3>Locations Added:</h3>
        <ul>
          {locations.map((loc, idx) => (
            <li key={idx}>
              Lat: {loc.lat}, Lng: {loc.lng}, Demand: {loc.demand}
            </li>
          ))}
        </ul>
      </div>

      <button onClick={handleOptimize} disabled={loading || locations.length === 0}>
        {loading ? "Optimizing..." : "Optimize VRP"}
      </button>

      {/* Show routes here after optimization */}
      {optimizedRoutes && (
        <div>
          <h3>Optimized Routes:</h3>
          {optimizedRoutes.map((route, idx) => (
            <div key={idx}>
              <h4>Vehicle {idx + 1}:</h4>
              <ul>
                {route.map((point, pidx) => (
                  <li key={pidx}>
                    Lat: {point.lat}, Lng: {point.lng}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
