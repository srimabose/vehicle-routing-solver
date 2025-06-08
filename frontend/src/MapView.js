import React from "react";
import { MapContainer, TileLayer, Marker, Popup, Polyline } from "react-leaflet";
import "leaflet/dist/leaflet.css";

const MapView = ({ coordinates }) => {
  if (coordinates.length === 0) return null;

  return (
    <MapContainer center={coordinates[0]} zoom={10} style={{ height: "500px", width: "100%" }}>
      <TileLayer
        attribution='&copy; OpenStreetMap contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {coordinates.map((pos, idx) => (
        <Marker key={idx} position={pos}>
          <Popup>Stop {idx + 1}</Popup>
        </Marker>
      ))}

      <Polyline positions={coordinates} color="blue" />
    </MapContainer>
  );
};

export default MapView;
